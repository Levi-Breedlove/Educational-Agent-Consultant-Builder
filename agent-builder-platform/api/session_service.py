#!/usr/bin/env python3
"""
Session Management Service
Handles session persistence in DynamoDB with TTL and automatic cleanup
"""

import boto3
import uuid
import logging
from datetime import datetime, timedelta
from typing import Optional, Dict, Any
from botocore.exceptions import ClientError

from .models import SessionStatus, WorkflowPhase, ExperienceLevel
from .config import settings

logger = logging.getLogger(__name__)


class SessionService:
    """Service for managing user sessions in DynamoDB"""
    
    def __init__(self):
        """Initialize DynamoDB client and table"""
        self.dynamodb = boto3.resource('dynamodb', region_name=settings.AWS_REGION)
        self.table_name = f"{settings.DYNAMODB_TABLE_PREFIX}-sessions"
        self.table = None
        self._initialize_table()
    
    def _initialize_table(self):
        """Initialize or get reference to DynamoDB table"""
        try:
            self.table = self.dynamodb.Table(self.table_name)
            # Verify table exists by describing it
            self.table.load()
            logger.info(f"Connected to DynamoDB table: {self.table_name}")
        except ClientError as e:
            if e.response['Error']['Code'] == 'ResourceNotFoundException':
                logger.warning(f"Table {self.table_name} not found, will create on first use")
                self.table = None
            else:
                logger.error(f"Error connecting to DynamoDB: {e}")
                raise
    
    def _ensure_table_exists(self):
        """Ensure the sessions table exists, create if not"""
        if self.table is not None:
            return
        
        try:
            # Create table with session_id as primary key
            table = self.dynamodb.create_table(
                TableName=self.table_name,
                KeySchema=[
                    {
                        'AttributeName': 'session_id',
                        'KeyType': 'HASH'  # Partition key
                    }
                ],
                AttributeDefinitions=[
                    {
                        'AttributeName': 'session_id',
                        'AttributeType': 'S'
                    },
                    {
                        'AttributeName': 'user_id',
                        'AttributeType': 'S'
                    }
                ],
                GlobalSecondaryIndexes=[
                    {
                        'IndexName': 'user_id-index',
                        'KeySchema': [
                            {
                                'AttributeName': 'user_id',
                                'KeyType': 'HASH'
                            }
                        ],
                        'Projection': {
                            'ProjectionType': 'ALL'
                        },
                        'ProvisionedThroughput': {
                            'ReadCapacityUnits': 5,
                            'WriteCapacityUnits': 5
                        }
                    }
                ],
                ProvisionedThroughput={
                    'ReadCapacityUnits': 5,
                    'WriteCapacityUnits': 5
                }
            )
            
            # Wait for table to be created
            table.wait_until_exists()
            
            # Enable TTL on the table
            dynamodb_client = boto3.client('dynamodb', region_name=settings.AWS_REGION)
            dynamodb_client.update_time_to_live(
                TableName=self.table_name,
                TimeToLiveSpecification={
                    'Enabled': True,
                    'AttributeName': 'ttl'
                }
            )
            
            self.table = table
            logger.info(f"Created DynamoDB table: {self.table_name}")
            
        except ClientError as e:
            if e.response['Error']['Code'] == 'ResourceInUseException':
                # Table already exists (race condition)
                self.table = self.dynamodb.Table(self.table_name)
                logger.info(f"Table {self.table_name} already exists")
            else:
                logger.error(f"Error creating table: {e}")
                raise
    
    def create_session(
        self,
        user_id: Optional[str] = None,
        experience_level: ExperienceLevel = ExperienceLevel.BEGINNER
    ) -> Dict[str, Any]:
        """
        Create a new session
        
        Args:
            user_id: Optional user identifier
            experience_level: User's experience level
            
        Returns:
            Session data dictionary
        """
        self._ensure_table_exists()
        
        session_id = f"session-{uuid.uuid4()}"
        now = datetime.utcnow()
        
        # Calculate TTL (24 hours from now)
        ttl = int((now + timedelta(hours=24)).timestamp())
        
        session_data = {
            'session_id': session_id,
            'user_id': user_id or f"anonymous-{uuid.uuid4()}",
            'status': SessionStatus.ACTIVE.value,
            'current_phase': WorkflowPhase.REQUIREMENTS.value,
            'experience_level': experience_level.value,
            'created_at': now.isoformat(),
            'updated_at': now.isoformat(),
            'ttl': ttl,
            'context': {},
            'workflow_state': {
                'requirements': None,
                'architecture': None,
                'implementation': None,
                'testing': None,
                'deployment': None
            },
            'progress_percentage': 0
        }
        
        try:
            self.table.put_item(Item=session_data)
            logger.info(f"Created session: {session_id}")
            return session_data
        except ClientError as e:
            logger.error(f"Error creating session: {e}")
            raise
    
    def get_session(self, session_id: str) -> Optional[Dict[str, Any]]:
        """
        Retrieve a session by ID
        
        Args:
            session_id: Session identifier
            
        Returns:
            Session data or None if not found
        """
        self._ensure_table_exists()
        
        try:
            response = self.table.get_item(Key={'session_id': session_id})
            session_data = response.get('Item')
            
            if session_data:
                logger.info(f"Retrieved session: {session_id}")
                return session_data
            else:
                logger.warning(f"Session not found: {session_id}")
                return None
                
        except ClientError as e:
            logger.error(f"Error retrieving session: {e}")
            raise
    
    def update_session(
        self,
        session_id: str,
        updates: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Update session data
        
        Args:
            session_id: Session identifier
            updates: Dictionary of fields to update
            
        Returns:
            Updated session data
        """
        self._ensure_table_exists()
        
        # Add updated_at timestamp
        updates['updated_at'] = datetime.utcnow().isoformat()
        
        # Build update expression
        update_expr_parts = []
        expr_attr_names = {}
        expr_attr_values = {}
        
        for key, value in updates.items():
            placeholder = f"#{key}"
            value_placeholder = f":{key}"
            update_expr_parts.append(f"{placeholder} = {value_placeholder}")
            expr_attr_names[placeholder] = key
            expr_attr_values[value_placeholder] = value
        
        update_expression = "SET " + ", ".join(update_expr_parts)
        
        try:
            response = self.table.update_item(
                Key={'session_id': session_id},
                UpdateExpression=update_expression,
                ExpressionAttributeNames=expr_attr_names,
                ExpressionAttributeValues=expr_attr_values,
                ReturnValues='ALL_NEW'
            )
            
            updated_data = response.get('Attributes', {})
            logger.info(f"Updated session: {session_id}")
            return updated_data
            
        except ClientError as e:
            logger.error(f"Error updating session: {e}")
            raise
    
    def delete_session(self, session_id: str) -> bool:
        """
        Delete a session
        
        Args:
            session_id: Session identifier
            
        Returns:
            True if deleted successfully
        """
        self._ensure_table_exists()
        
        try:
            self.table.delete_item(Key={'session_id': session_id})
            logger.info(f"Deleted session: {session_id}")
            return True
        except ClientError as e:
            logger.error(f"Error deleting session: {e}")
            raise
    
    def cleanup_expired_sessions(self) -> int:
        """
        Manually cleanup expired sessions (TTL handles this automatically)
        This is a backup method for immediate cleanup if needed
        
        Returns:
            Number of sessions cleaned up
        """
        self._ensure_table_exists()
        
        try:
            now = int(datetime.utcnow().timestamp())
            
            # Scan for expired sessions
            response = self.table.scan(
                FilterExpression='#ttl < :now',
                ExpressionAttributeNames={'#ttl': 'ttl'},
                ExpressionAttributeValues={':now': now}
            )
            
            expired_sessions = response.get('Items', [])
            count = 0
            
            for session in expired_sessions:
                self.delete_session(session['session_id'])
                count += 1
            
            logger.info(f"Cleaned up {count} expired sessions")
            return count
            
        except ClientError as e:
            logger.error(f"Error cleaning up sessions: {e}")
            raise
    
    def get_user_sessions(self, user_id: str) -> list:
        """
        Get all sessions for a user
        
        Args:
            user_id: User identifier
            
        Returns:
            List of session data
        """
        self._ensure_table_exists()
        
        try:
            response = self.table.query(
                IndexName='user_id-index',
                KeyConditionExpression='user_id = :user_id',
                ExpressionAttributeValues={':user_id': user_id}
            )
            
            sessions = response.get('Items', [])
            logger.info(f"Retrieved {len(sessions)} sessions for user: {user_id}")
            return sessions
            
        except ClientError as e:
            logger.error(f"Error retrieving user sessions: {e}")
            raise


# Global session service instance
_session_service: Optional[SessionService] = None


def get_session_service() -> SessionService:
    """Get or create session service instance"""
    global _session_service
    if _session_service is None:
        _session_service = SessionService()
    return _session_service
