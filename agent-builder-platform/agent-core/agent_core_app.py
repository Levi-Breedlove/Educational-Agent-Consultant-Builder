#!/usr/bin/env python3
"""
Agent Builder Platform - Agent Core Application
Main application entry point for the Agent Core framework
"""

import os
import json
import logging
from typing import Dict, Any, Optional
from dataclasses import dataclass, asdict
import boto3
from botocore.exceptions import ClientError

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class AWSConfig:
    """AWS configuration for the Agent Core application"""
    region: str = "us-east-1"
    s3_bucket_projects: str = "agent-builder-projects"
    s3_bucket_agents: str = "agent-builder-generated-agents"
    dynamodb_table_configs: str = "agent-configurations"
    dynamodb_table_metadata: str = "project-metadata"
    ecs_cluster_name: str = "agent-builder-cluster"
    ecs_service_name: str = "agent-core-service"
    
    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

@dataclass
class AgentCoreConfig:
    """Main configuration for Agent Core application"""
    project_name: str = "agent-builder-platform"
    environment: str = "dev"
    aws_config: AWSConfig = None
    log_level: str = "INFO"
    
    def __post_init__(self):
        if self.aws_config is None:
            self.aws_config = AWSConfig()
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'project_name': self.project_name,
            'environment': self.environment,
            'aws_config': self.aws_config.to_dict(),
            'log_level': self.log_level
        }

class AgentCoreApp:
    """
    Main Agent Core application class
    Handles initialization, configuration, and AWS service setup
    """
    
    def __init__(self, config: Optional[AgentCoreConfig] = None):
        self.config = config or AgentCoreConfig()
        self.aws_clients = {}
        self.initialized = False
        
        logger.info(f"Agent Core App initializing for {self.config.project_name}-{self.config.environment}")
    
    def initialize(self) -> bool:
        """Initialize the Agent Core application"""
        try:
            logger.info("Initializing Agent Core application...")
            
            # Initialize AWS clients (mock for development)
            self._initialize_aws_clients()
            
            # Validate configuration
            self._validate_configuration()
            
            # Initialize storage schemas (conceptual - no actual AWS calls)
            self._initialize_storage_schemas()
            
            self.initialized = True
            logger.info("✅ Agent Core application initialized successfully")
            return True
            
        except Exception as e:
            logger.error(f"❌ Failed to initialize Agent Core application: {e}")
            return False
    
    def _initialize_aws_clients(self):
        """Initialize AWS service clients (mock for development)"""
        try:
            # In a real deployment, these would be actual boto3 clients
            # For development, we'll create mock clients
            self.aws_clients = {
                's3': MockS3Client(self.config.aws_config),
                'dynamodb': MockDynamoDBClient(self.config.aws_config),
                'ecs': MockECSClient(self.config.aws_config)
            }
            logger.info("✅ AWS clients initialized (mock mode)")
            
        except Exception as e:
            logger.error(f"❌ Failed to initialize AWS clients: {e}")
            raise
    
    def _validate_configuration(self):
        """Validate the application configuration"""
        required_fields = ['project_name', 'environment']
        
        for field in required_fields:
            if not getattr(self.config, field):
                raise ValueError(f"Required configuration field '{field}' is missing")
        
        # Validate AWS configuration
        aws_config = self.config.aws_config
        if not aws_config.region:
            raise ValueError("AWS region is required")
        
        logger.info("✅ Configuration validated")
    
    def _initialize_storage_schemas(self):
        """Initialize storage schemas for S3 and DynamoDB"""
        try:
            # S3 bucket schemas (conceptual)
            s3_schemas = {
                'projects': {
                    'bucket': self.config.aws_config.s3_bucket_projects,
                    'structure': {
                        'users/{user_id}/projects/{project_id}/': 'Project files',
                        'users/{user_id}/projects/{project_id}/requirements.json': 'Requirements',
                        'users/{user_id}/projects/{project_id}/architecture.json': 'Architecture',
                        'users/{user_id}/projects/{project_id}/implementation/': 'Implementation files'
                    }
                },
                'agents': {
                    'bucket': self.config.aws_config.s3_bucket_agents,
                    'structure': {
                        'generated/{project_id}/': 'Generated agent files',
                        'generated/{project_id}/agent.py': 'Main agent code',
                        'generated/{project_id}/config.json': 'Agent configuration',
                        'generated/{project_id}/requirements.txt': 'Dependencies'
                    }
                }
            }
            
            # DynamoDB table schemas (conceptual)
            dynamodb_schemas = {
                'agent_configurations': {
                    'table_name': self.config.aws_config.dynamodb_table_configs,
                    'partition_key': 'project_id',
                    'sort_key': 'config_type',
                    'attributes': {
                        'project_id': 'String',
                        'config_type': 'String',  # 'requirements', 'architecture', 'implementation'
                        'config_data': 'Map',
                        'created_at': 'String',
                        'updated_at': 'String',
                        'version': 'Number'
                    }
                },
                'project_metadata': {
                    'table_name': self.config.aws_config.dynamodb_table_metadata,
                    'partition_key': 'user_id',
                    'sort_key': 'project_id',
                    'attributes': {
                        'user_id': 'String',
                        'project_id': 'String',
                        'project_name': 'String',
                        'status': 'String',
                        'created_at': 'String',
                        'updated_at': 'String',
                        'workflow_phase': 'String'
                    }
                }
            }
            
            # Store schemas for reference
            self.storage_schemas = {
                's3': s3_schemas,
                'dynamodb': dynamodb_schemas
            }
            
            logger.info("✅ Storage schemas initialized")
            
        except Exception as e:
            logger.error(f"❌ Failed to initialize storage schemas: {e}")
            raise
    
    def get_config(self) -> Dict[str, Any]:
        """Get the current configuration"""
        return self.config.to_dict()
    
    def get_aws_client(self, service: str):
        """Get an AWS service client"""
        if service not in self.aws_clients:
            raise ValueError(f"AWS client for service '{service}' not available")
        return self.aws_clients[service]
    
    def is_initialized(self) -> bool:
        """Check if the application is initialized"""
        return self.initialized

# Mock AWS clients for development
class MockS3Client:
    """Mock S3 client for development"""
    
    def __init__(self, aws_config: AWSConfig):
        self.config = aws_config
        logger.info(f"Mock S3 client initialized for buckets: {aws_config.s3_bucket_projects}, {aws_config.s3_bucket_agents}")
    
    def create_bucket(self, bucket_name: str):
        logger.info(f"Mock: Would create S3 bucket '{bucket_name}'")
        return True
    
    def put_object(self, bucket: str, key: str, body: str):
        logger.info(f"Mock: Would put object '{key}' in bucket '{bucket}'")
        return True

class MockDynamoDBClient:
    """Mock DynamoDB client for development"""
    
    def __init__(self, aws_config: AWSConfig):
        self.config = aws_config
        logger.info(f"Mock DynamoDB client initialized for tables: {aws_config.dynamodb_table_configs}, {aws_config.dynamodb_table_metadata}")
    
    def create_table(self, table_name: str, schema: Dict[str, Any]):
        logger.info(f"Mock: Would create DynamoDB table '{table_name}' with schema")
        return True
    
    def put_item(self, table_name: str, item: Dict[str, Any]):
        logger.info(f"Mock: Would put item in table '{table_name}'")
        return True

class MockECSClient:
    """Mock ECS client for development"""
    
    def __init__(self, aws_config: AWSConfig):
        self.config = aws_config
        logger.info(f"Mock ECS client initialized for cluster: {aws_config.ecs_cluster_name}")
    
    def create_cluster(self, cluster_name: str):
        logger.info(f"Mock: Would create ECS cluster '{cluster_name}'")
        return True
    
    def create_service(self, cluster: str, service_name: str):
        logger.info(f"Mock: Would create ECS service '{service_name}' in cluster '{cluster}'")
        return True

# Test function
def test_agent_core_app():
    """Test the Agent Core application"""
    try:
        print("🚀 Testing Agent Core App...")
        
        # Create configuration
        config = AgentCoreConfig(
            project_name="agent-builder-platform",
            environment="dev"
        )
        
        # Create and initialize app
        app = AgentCoreApp(config)
        
        if app.initialize():
            print("✅ Agent Core App initialized successfully")
            
            # Test configuration access
            config_dict = app.get_config()
            print(f"✅ Configuration: {config_dict['project_name']}-{config_dict['environment']}")
            
            # Test AWS client access
            s3_client = app.get_aws_client('s3')
            dynamodb_client = app.get_aws_client('dynamodb')
            ecs_client = app.get_aws_client('ecs')
            
            print("✅ AWS clients accessible")
            
            # Test mock operations
            s3_client.create_bucket("test-bucket")
            dynamodb_client.create_table("test-table", {})
            ecs_client.create_cluster("test-cluster")
            
            print("✅ Mock AWS operations working")
            print("🎉 Agent Core App test completed successfully!")
            return True
        else:
            print("❌ Agent Core App initialization failed")
            return False
            
    except Exception as e:
        print(f"❌ Agent Core App test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    test_agent_core_app()