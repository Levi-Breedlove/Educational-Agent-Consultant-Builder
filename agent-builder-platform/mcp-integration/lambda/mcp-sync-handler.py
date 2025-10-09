"""
MCP Knowledge Synchronization Lambda Handler
Synchronizes knowledge from various MCPs to DynamoDB for reliable offline access
"""

import json
import boto3
import logging
import os
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
import asyncio
import aiohttp
from botocore.exceptions import ClientError

# Configure logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# AWS clients
dynamodb = boto3.resource('dynamodb')
bedrock_client = boto3.client('bedrock-runtime', region_name='us-east-1')
sns = boto3.client('sns')
cloudwatch = boto3.client('cloudwatch')

# Environment variables
PROJECT_NAME = os.environ.get('PROJECT_NAME', 'agent-builder-platform')
ENVIRONMENT = os.environ.get('ENVIRONMENT', 'dev')
SNS_TOPIC_ARN = os.environ.get('SNS_TOPIC_ARN')
GITHUB_TOKEN = os.environ.get('GITHUB_TOKEN')

class MCPSyncHandler:
    """Handles synchronization of knowledge from MCPs to DynamoDB with vector search"""
    
    def __init__(self):
        self.aws_knowledge_table = dynamodb.Table(f'{PROJECT_NAME}-aws-knowledge-{ENVIRONMENT}')
        self.strands_knowledge_table = dynamodb.Table(f'{PROJECT_NAME}-strands-knowledge-{ENVIRONMENT}')
        self.mcp_repository_table = dynamodb.Table(f'{PROJECT_NAME}-mcp-repository-{ENVIRONMENT}')
        
        # Vector search configuration
        self.embedding_model = "amazon.titan-embed-text-v1"
        self.vector_dimension = 1536
        self.enable_embeddings = os.environ.get('ENABLE_EMBEDDINGS', 'true').lower() == 'true'
        
    async def generate_embedding(self, text: str) -> Optional[List[float]]:
        """Generate embedding using Amazon Bedrock Titan"""
        if not self.enable_embeddings:
            return None
            
        try:
            # Prepare text for embedding (limit to 8000 tokens)
            processed_text = text[:8000] if len(text) > 8000 else text
            processed_text = processed_text.strip()
            
            # Generate embedding via Bedrock
            response = bedrock_client.invoke_model(
                modelId=self.embedding_model,
                body=json.dumps({
                    'inputText': processed_text
                })
            )
            
            # Parse response
            response_body = json.loads(response['body'].read())
            embedding = response_body.get('embedding')
            
            if embedding and len(embedding) == self.vector_dimension:
                logger.debug(f"Generated embedding with {len(embedding)} dimensions")
                return embedding
            else:
                logger.warning(f"Invalid embedding response: {len(embedding) if embedding else 0} dimensions")
                return None
                
        except ClientError as e:
            logger.error(f"Bedrock embedding generation failed: {e}")
            return None
        except Exception as e:
            logger.error(f"Unexpected error in embedding generation: {e}")
            return None
        
    async def sync_aws_documentation(self) -> Dict[str, Any]:
        """Synchronize AWS documentation from AWS docs MCP"""
        logger.info("Starting AWS documentation synchronization")
        
        try:
            # Simulate AWS docs MCP integration
            # In real implementation, this would call the actual MCP
            aws_docs_data = await self._fetch_aws_documentation()
            
            # Process and store in DynamoDB
            sync_results = {
                'synced_items': 0,
                'failed_items': 0,
                'categories': []
            }
            
            for category, items in aws_docs_data.items():
                sync_results['categories'].append(category)
                
                for item in items:
                    try:
                        # Store in DynamoDB with TTL
                        ttl = int((datetime.now() + timedelta(days=7)).timestamp())
                        
                        # Generate embedding for semantic search
                        embedding = await self._generate_embedding(f"{item['title']} {item['content']}")
                        
                        self.aws_knowledge_table.put_item(
                            Item={
                                'category': category,
                                'item_id': item['id'],
                                'title': item['title'],
                                'content': item['content'],
                                'url': item.get('url', ''),
                                'embedding': json.dumps(embedding) if embedding else None,
                                'embedding_model': 'amazon.titan-embed-text-v1',
                                'last_updated': datetime.now().isoformat(),
                                'ttl': ttl,
                                'source': 'aws_docs_mcp',
                                'confidence_score': item.get('confidence', 0.9)
                            }
                        )
                        sync_results['synced_items'] += 1
                        
                    except Exception as e:
                        logger.error(f"Failed to sync AWS doc item {item['id']}: {str(e)}")
                        sync_results['failed_items'] += 1
            
            logger.info(f"AWS docs sync completed: {sync_results}")
            return sync_results
            
        except Exception as e:
            logger.error(f"AWS documentation sync failed: {str(e)}")
            await self._send_alert("AWS Documentation Sync Failed", str(e))
            raise
    
    async def sync_strands_knowledge(self) -> Dict[str, Any]:
        """Synchronize Strands agent knowledge from Strands MCP"""
        logger.info("Starting Strands knowledge synchronization")
        
        try:
            # Simulate Strands MCP integration
            strands_data = await self._fetch_strands_knowledge()
            
            sync_results = {
                'synced_items': 0,
                'failed_items': 0,
                'categories': []
            }
            
            for category, items in strands_data.items():
                sync_results['categories'].append(category)
                
                for item in items:
                    try:
                        ttl = int((datetime.now() + timedelta(days=7)).timestamp())
                        
                        self.strands_knowledge_table.put_item(
                            Item={
                                'category': category,
                                'item_id': item['id'],
                                'name': item['name'],
                                'description': item['description'],
                                'template': item.get('template', ''),
                                'capabilities': item.get('capabilities', []),
                                'examples': item.get('examples', []),
                                'last_updated': datetime.now().isoformat(),
                                'ttl': ttl,
                                'source': 'strands_mcp',
                                'confidence_score': item.get('confidence', 0.9)
                            }
                        )
                        sync_results['synced_items'] += 1
                        
                    except Exception as e:
                        logger.error(f"Failed to sync Strands item {item['id']}: {str(e)}")
                        sync_results['failed_items'] += 1
            
            logger.info(f"Strands sync completed: {sync_results}")
            return sync_results
            
        except Exception as e:
            logger.error(f"Strands knowledge sync failed: {str(e)}")
            await self._send_alert("Strands Knowledge Sync Failed", str(e))
            raise
    
    async def sync_mcp_repositories(self) -> Dict[str, Any]:
        """Synchronize MCP repository information from GitHub MCP"""
        logger.info("Starting MCP repository synchronization")
        
        try:
            # Simulate GitHub MCP integration
            mcp_repos_data = await self._fetch_mcp_repositories()
            
            sync_results = {
                'synced_items': 0,
                'failed_items': 0,
                'repositories': []
            }
            
            for repo in mcp_repos_data:
                try:
                    ttl = int((datetime.now() + timedelta(days=14)).timestamp())
                    
                    self.mcp_repository_table.put_item(
                        Item={
                            'repository_name': repo['name'],
                            'last_updated': datetime.now().isoformat(),
                            'description': repo['description'],
                            'stars': repo.get('stars', 0),
                            'language': repo.get('language', ''),
                            'capabilities': repo.get('capabilities', []),
                            'compatibility': repo.get('compatibility', {}),
                            'usage_examples': repo.get('examples', []),
                            'ttl': ttl,
                            'source': 'github_mcp',
                            'confidence_score': repo.get('confidence', 0.8)
                        }
                    )
                    sync_results['synced_items'] += 1
                    sync_results['repositories'].append(repo['name'])
                    
                except Exception as e:
                    logger.error(f"Failed to sync MCP repo {repo['name']}: {str(e)}")
                    sync_results['failed_items'] += 1
            
            logger.info(f"MCP repositories sync completed: {sync_results}")
            return sync_results
            
        except Exception as e:
            logger.error(f"MCP repositories sync failed: {str(e)}")
            await self._send_alert("MCP Repositories Sync Failed", str(e))
            raise
    
    async def _fetch_aws_documentation(self) -> Dict[str, List[Dict]]:
        """Fetch AWS documentation data (simulated MCP call)"""
        # In real implementation, this would call the AWS docs MCP
        return {
            'service_documentation': [
                {
                    'id': 'ec2-overview',
                    'title': 'Amazon EC2 Overview',
                    'content': 'Amazon Elastic Compute Cloud (EC2) provides scalable computing capacity...',
                    'url': 'https://docs.aws.amazon.com/ec2/',
                    'confidence': 0.95
                },
                {
                    'id': 's3-overview',
                    'title': 'Amazon S3 Overview',
                    'content': 'Amazon Simple Storage Service (S3) is an object storage service...',
                    'url': 'https://docs.aws.amazon.com/s3/',
                    'confidence': 0.95
                }
            ],
            'best_practices': [
                {
                    'id': 'security-best-practices',
                    'title': 'AWS Security Best Practices',
                    'content': 'Follow these security best practices for AWS deployments...',
                    'url': 'https://docs.aws.amazon.com/security/',
                    'confidence': 0.9
                }
            ],
            'pricing_information': [
                {
                    'id': 'ec2-pricing',
                    'title': 'EC2 Pricing',
                    'content': 'EC2 pricing varies by instance type, region, and usage...',
                    'url': 'https://aws.amazon.com/ec2/pricing/',
                    'confidence': 0.85
                }
            ]
        }
    
    async def _fetch_strands_knowledge(self) -> Dict[str, List[Dict]]:
        """Fetch Strands knowledge data (simulated MCP call)"""
        return {
            'agent_templates': [
                {
                    'id': 'basic-chatbot',
                    'name': 'Basic Chatbot Template',
                    'description': 'A simple chatbot template with basic conversation capabilities',
                    'template': '{"type": "chatbot", "capabilities": ["conversation"]}',
                    'confidence': 0.9
                },
                {
                    'id': 'data-analyst',
                    'name': 'Data Analysis Agent',
                    'description': 'Agent specialized in data analysis and visualization',
                    'template': '{"type": "analyst", "capabilities": ["data_analysis", "visualization"]}',
                    'confidence': 0.85
                }
            ],
            'capabilities': [
                {
                    'id': 'natural-language-processing',
                    'name': 'Natural Language Processing',
                    'description': 'Advanced NLP capabilities for text understanding',
                    'examples': ['sentiment analysis', 'entity extraction'],
                    'confidence': 0.9
                }
            ]
        }
    
    async def _fetch_mcp_repositories(self) -> List[Dict]:
        """Fetch MCP repository data (simulated GitHub MCP call)"""
        return [
            {
                'name': 'filesystem-mcp',
                'description': 'MCP server for filesystem operations',
                'stars': 150,
                'language': 'Python',
                'capabilities': ['file_read', 'file_write', 'directory_list'],
                'compatibility': {'agent_core': True, 'strands': True},
                'confidence': 0.9
            },
            {
                'name': 'web-search-mcp',
                'description': 'MCP server for web search capabilities',
                'stars': 200,
                'language': 'TypeScript',
                'capabilities': ['web_search', 'url_fetch', 'content_extract'],
                'compatibility': {'agent_core': True, 'strands': True},
                'confidence': 0.85
            }
        ]
    
    async def _send_alert(self, subject: str, message: str):
        """Send alert notification via SNS"""
        if SNS_TOPIC_ARN:
            try:
                sns.publish(
                    TopicArn=SNS_TOPIC_ARN,
                    Subject=f"[{PROJECT_NAME}] {subject}",
                    Message=message
                )
            except Exception as e:
                logger.error(f"Failed to send SNS alert: {str(e)}")
    
    def _publish_metrics(self, sync_type: str, synced_items: int, failed_items: int):
        """Publish metrics to CloudWatch"""
        try:
            cloudwatch.put_metric_data(
                Namespace=f'{PROJECT_NAME}/MCP-Sync',
                MetricData=[
                    {
                        'MetricName': 'SyncedItems',
                        'Dimensions': [
                            {
                                'Name': 'SyncType',
                                'Value': sync_type
                            }
                        ],
                        'Value': synced_items,
                        'Unit': 'Count'
                    },
                    {
                        'MetricName': 'FailedItems',
                        'Dimensions': [
                            {
                                'Name': 'SyncType',
                                'Value': sync_type
                            }
                        ],
                        'Value': failed_items,
                        'Unit': 'Count'
                    }
                ]
            )
        except Exception as e:
            logger.error(f"Failed to publish metrics: {str(e)}")
    
    async def _generate_embedding(self, text: str) -> Optional[List[float]]:
        """Generate embedding using Amazon Bedrock Titan"""
        try:
            # Initialize Bedrock client if not exists
            if not hasattr(self, 'bedrock_client'):
                self.bedrock_client = boto3.client('bedrock-runtime')
            
            # Limit text length for embedding model
            text_content = text[:8000] if len(text) > 8000 else text
            
            response = self.bedrock_client.invoke_model(
                modelId='amazon.titan-embed-text-v1',
                body=json.dumps({
                    'inputText': text_content
                })
            )
            
            response_body = json.loads(response['body'].read())
            return response_body.get('embedding')
            
        except Exception as e:
            logger.warning(f"Failed to generate embedding: {str(e)}")
            return None

async def lambda_handler(event, context):
    """Main Lambda handler for MCP synchronization"""
    logger.info(f"Starting MCP sync with event: {json.dumps(event)}")
    
    sync_handler = MCPSyncHandler()
    results = {
        'sync_timestamp': datetime.now().isoformat(),
        'results': {}
    }
    
    try:
        # Determine which sync to run based on event
        sync_type = event.get('sync_type', 'all')
        
        if sync_type in ['all', 'aws']:
            aws_results = await sync_handler.sync_aws_documentation()
            results['results']['aws_documentation'] = aws_results
            sync_handler._publish_metrics('aws_documentation', 
                                        aws_results['synced_items'], 
                                        aws_results['failed_items'])
        
        if sync_type in ['all', 'strands']:
            strands_results = await sync_handler.sync_strands_knowledge()
            results['results']['strands_knowledge'] = strands_results
            sync_handler._publish_metrics('strands_knowledge', 
                                        strands_results['synced_items'], 
                                        strands_results['failed_items'])
        
        if sync_type in ['all', 'mcp_repos']:
            mcp_results = await sync_handler.sync_mcp_repositories()
            results['results']['mcp_repositories'] = mcp_results
            sync_handler._publish_metrics('mcp_repositories', 
                                        mcp_results['synced_items'], 
                                        mcp_results['failed_items'])
        
        logger.info(f"MCP sync completed successfully: {results}")
        
        return {
            'statusCode': 200,
            'body': json.dumps(results)
        }
        
    except Exception as e:
        logger.error(f"MCP sync failed: {str(e)}")
        
        return {
            'statusCode': 500,
            'body': json.dumps({
                'error': str(e),
                'sync_timestamp': datetime.now().isoformat()
            })
        }

# For local testing
if __name__ == "__main__":
    import asyncio
    
    # Test event
    test_event = {'sync_type': 'all'}
    test_context = {}
    
    result = asyncio.run(lambda_handler(test_event, test_context))
    print(json.dumps(result, indent=2))