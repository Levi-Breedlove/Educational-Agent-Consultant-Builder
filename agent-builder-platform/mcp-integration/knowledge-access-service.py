"""
Hybrid Knowledge Access Service
Provides intelligent routing between cached knowledge base and real-time MCP calls
"""

import json
import boto3
import logging
import asyncio
import aiohttp
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Union
from dataclasses import dataclass
from enum import Enum
import hashlib

logger = logging.getLogger(__name__)

class QueryType(Enum):
    DOCUMENTATION = "documentation"
    PRICING = "pricing"
    BEST_PRACTICES = "best_practices"
    AGENT_TEMPLATES = "agent_templates"
    MCP_REPOSITORIES = "mcp_repositories"
    CAPABILITIES = "capabilities"

class DataSource(Enum):
    CACHED = "cached"
    REALTIME = "realtime"
    HYBRID = "hybrid"

@dataclass
class KnowledgeQuery:
    query_text: str
    query_type: QueryType
    user_context: Dict[str, Any]
    max_results: int = 10
    freshness_required: bool = False

@dataclass
class KnowledgeResult:
    content: Any
    source: DataSource
    confidence_score: float
    freshness: datetime
    metadata: Dict[str, Any]

class HybridKnowledgeAccessService:
    """
    Intelligent knowledge access service that routes queries between
    cached knowledge base and real-time MCP calls based on:
    - Data freshness requirements
    - Query type characteristics
    - MCP availability
    - Cost optimization
    """
    
    def __init__(self, project_name: str, environment: str):
        self.project_name = project_name
        self.environment = environment
        
        # AWS clients
        self.dynamodb = boto3.resource('dynamodb')
        self.cloudwatch = boto3.client('cloudwatch')
        
        # DynamoDB tables
        self.aws_knowledge_table = self.dynamodb.Table(f'{project_name}-aws-knowledge-{environment}')
        self.strands_knowledge_table = self.dynamodb.Table(f'{project_name}-strands-knowledge-{environment}')
        self.mcp_repository_table = self.dynamodb.Table(f'{project_name}-mcp-repository-{environment}')
        
        # Configuration
        self.freshness_threshold = timedelta(hours=24)
        self.mcp_timeout = 5  # seconds
        self.confidence_threshold = 0.7
        
        # Routing rules
        self.routing_rules = {
            QueryType.PRICING: DataSource.REALTIME,  # Pricing changes frequently
            QueryType.DOCUMENTATION: DataSource.CACHED,  # Documentation is stable
            QueryType.BEST_PRACTICES: DataSource.CACHED,  # Best practices are stable
            QueryType.AGENT_TEMPLATES: DataSource.CACHED,  # Templates are relatively stable
            QueryType.MCP_REPOSITORIES: DataSource.HYBRID,  # Mix of stable and changing data
            QueryType.CAPABILITIES: DataSource.CACHED  # Capabilities are stable
        }
    
    async def query_knowledge(self, query: KnowledgeQuery) -> List[KnowledgeResult]:
        """
        Main entry point for knowledge queries with intelligent routing
        """
        logger.info(f"Processing knowledge query: {query.query_type.value} - {query.query_text[:100]}")
        
        try:
            # Determine optimal data source
            preferred_source = self._determine_data_source(query)
            
            # Execute query based on routing decision
            if preferred_source == DataSource.CACHED:
                results = await self._query_cached_knowledge(query)
                
                # Fallback to real-time if cached results are insufficient
                if not results or self._needs_realtime_fallback(results, query):
                    logger.info("Falling back to real-time MCP due to insufficient cached results")
                    realtime_results = await self._query_realtime_mcp(query)
                    results.extend(realtime_results)
                    
            elif preferred_source == DataSource.REALTIME:
                results = await self._query_realtime_mcp(query)
                
                # Fallback to cached if real-time fails
                if not results:
                    logger.info("Falling back to cached knowledge due to MCP failure")
                    results = await self._query_cached_knowledge(query)
                    
            else:  # HYBRID
                # Execute both in parallel and merge results
                cached_task = asyncio.create_task(self._query_cached_knowledge(query))
                realtime_task = asyncio.create_task(self._query_realtime_mcp(query))
                
                cached_results, realtime_results = await asyncio.gather(
                    cached_task, realtime_task, return_exceptions=True
                )
                
                # Handle exceptions
                if isinstance(cached_results, Exception):
                    cached_results = []
                if isinstance(realtime_results, Exception):
                    realtime_results = []
                
                results = self._merge_results(cached_results, realtime_results, query)
            
            # Post-process results
            results = self._post_process_results(results, query)
            
            # Record metrics
            self._record_query_metrics(query, results, preferred_source)
            
            logger.info(f"Query completed: {len(results)} results from {preferred_source.value}")
            return results
            
        except Exception as e:
            logger.error(f"Knowledge query failed: {str(e)}")
            # Emergency fallback to cached data
            try:
                return await self._query_cached_knowledge(query)
            except:
                return []
    
    def _determine_data_source(self, query: KnowledgeQuery) -> DataSource:
        """Determine optimal data source based on query characteristics"""
        
        # Check if freshness is explicitly required
        if query.freshness_required:
            return DataSource.REALTIME
        
        # Apply routing rules based on query type
        preferred_source = self.routing_rules.get(query.query_type, DataSource.CACHED)
        
        # Override for specific patterns
        if "price" in query.query_text.lower() or "cost" in query.query_text.lower():
            return DataSource.REALTIME
        
        if "latest" in query.query_text.lower() or "current" in query.query_text.lower():
            return DataSource.REALTIME
        
        return preferred_source
    
    async def _query_cached_knowledge(self, query: KnowledgeQuery) -> List[KnowledgeResult]:
        """Query cached knowledge from DynamoDB"""
        results = []
        
        try:
            if query.query_type in [QueryType.DOCUMENTATION, QueryType.BEST_PRACTICES, QueryType.PRICING]:
                # Query AWS knowledge table
                results.extend(await self._query_aws_knowledge(query))
                
            elif query.query_type in [QueryType.AGENT_TEMPLATES, QueryType.CAPABILITIES]:
                # Query Strands knowledge table
                results.extend(await self._query_strands_knowledge(query))
                
            elif query.query_type == QueryType.MCP_REPOSITORIES:
                # Query MCP repository table
                results.extend(await self._query_mcp_repositories(query))
            
            return results
            
        except Exception as e:
            logger.error(f"Cached knowledge query failed: {str(e)}")
            return []
    
    async def _query_aws_knowledge(self, query: KnowledgeQuery) -> List[KnowledgeResult]:
        """Query AWS knowledge from DynamoDB"""
        results = []
        
        try:
            # Determine category based on query type
            category = {
                QueryType.DOCUMENTATION: "service_documentation",
                QueryType.BEST_PRACTICES: "best_practices",
                QueryType.PRICING: "pricing_information"
            }.get(query.query_type, "service_documentation")
            
            # Query DynamoDB
            response = self.aws_knowledge_table.query(
                KeyConditionExpression=boto3.dynamodb.conditions.Key('category').eq(category),
                Limit=query.max_results
            )
            
            for item in response.get('Items', []):
                # Simple text matching (in production, use more sophisticated search)
                if self._matches_query(query.query_text, item.get('title', '') + ' ' + item.get('content', '')):
                    result = KnowledgeResult(
                        content={
                            'title': item.get('title'),
                            'content': item.get('content'),
                            'url': item.get('url')
                        },
                        source=DataSource.CACHED,
                        confidence_score=item.get('confidence_score', 0.8),
                        freshness=datetime.fromisoformat(item.get('last_updated')),
                        metadata={
                            'category': category,
                            'source_mcp': item.get('source'),
                            'item_id': item.get('item_id')
                        }
                    )
                    results.append(result)
            
            return results
            
        except Exception as e:
            logger.error(f"AWS knowledge query failed: {str(e)}")
            return []
    
    async def _query_strands_knowledge(self, query: KnowledgeQuery) -> List[KnowledgeResult]:
        """Query Strands knowledge from DynamoDB"""
        results = []
        
        try:
            category = {
                QueryType.AGENT_TEMPLATES: "agent_templates",
                QueryType.CAPABILITIES: "capabilities"
            }.get(query.query_type, "agent_templates")
            
            response = self.strands_knowledge_table.query(
                KeyConditionExpression=boto3.dynamodb.conditions.Key('category').eq(category),
                Limit=query.max_results
            )
            
            for item in response.get('Items', []):
                if self._matches_query(query.query_text, item.get('name', '') + ' ' + item.get('description', '')):
                    result = KnowledgeResult(
                        content={
                            'name': item.get('name'),
                            'description': item.get('description'),
                            'template': item.get('template'),
                            'capabilities': item.get('capabilities', []),
                            'examples': item.get('examples', [])
                        },
                        source=DataSource.CACHED,
                        confidence_score=item.get('confidence_score', 0.8),
                        freshness=datetime.fromisoformat(item.get('last_updated')),
                        metadata={
                            'category': category,
                            'source_mcp': item.get('source'),
                            'item_id': item.get('item_id')
                        }
                    )
                    results.append(result)
            
            return results
            
        except Exception as e:
            logger.error(f"Strands knowledge query failed: {str(e)}")
            return []
    
    async def _query_mcp_repositories(self, query: KnowledgeQuery) -> List[KnowledgeResult]:
        """Query MCP repositories from DynamoDB"""
        results = []
        
        try:
            # Scan table for matching repositories (in production, use GSI for better performance)
            response = self.mcp_repository_table.scan(
                Limit=query.max_results
            )
            
            for item in response.get('Items', []):
                if self._matches_query(query.query_text, item.get('repository_name', '') + ' ' + item.get('description', '')):
                    result = KnowledgeResult(
                        content={
                            'name': item.get('repository_name'),
                            'description': item.get('description'),
                            'stars': item.get('stars', 0),
                            'language': item.get('language'),
                            'capabilities': item.get('capabilities', []),
                            'compatibility': item.get('compatibility', {}),
                            'usage_examples': item.get('usage_examples', [])
                        },
                        source=DataSource.CACHED,
                        confidence_score=item.get('confidence_score', 0.8),
                        freshness=datetime.fromisoformat(item.get('last_updated')),
                        metadata={
                            'source_mcp': item.get('source'),
                            'repository_name': item.get('repository_name')
                        }
                    )
                    results.append(result)
            
            return results
            
        except Exception as e:
            logger.error(f"MCP repositories query failed: {str(e)}")
            return []
    
    async def _query_realtime_mcp(self, query: KnowledgeQuery) -> List[KnowledgeResult]:
        """Query real-time MCP services"""
        results = []
        
        try:
            # Simulate MCP calls (in production, use actual MCP clients)
            if query.query_type in [QueryType.DOCUMENTATION, QueryType.BEST_PRACTICES, QueryType.PRICING]:
                results.extend(await self._call_aws_docs_mcp(query))
                
            elif query.query_type in [QueryType.AGENT_TEMPLATES, QueryType.CAPABILITIES]:
                results.extend(await self._call_strands_mcp(query))
                
            elif query.query_type == QueryType.MCP_REPOSITORIES:
                results.extend(await self._call_github_mcp(query))
            
            return results
            
        except asyncio.TimeoutError:
            logger.warning("MCP query timed out")
            return []
        except Exception as e:
            logger.error(f"Real-time MCP query failed: {str(e)}")
            return []
    
    async def _call_aws_docs_mcp(self, query: KnowledgeQuery) -> List[KnowledgeResult]:
        """Call AWS documentation MCP (simulated)"""
        # Simulate MCP call with timeout
        await asyncio.sleep(0.1)  # Simulate network delay
        
        # Return simulated real-time results
        return [
            KnowledgeResult(
                content={
                    'title': f'Real-time AWS Documentation for: {query.query_text}',
                    'content': 'This is real-time AWS documentation content...',
                    'url': 'https://docs.aws.amazon.com/...'
                },
                source=DataSource.REALTIME,
                confidence_score=0.9,
                freshness=datetime.now(),
                metadata={'source_mcp': 'aws_docs_mcp', 'realtime': True}
            )
        ]
    
    async def _call_strands_mcp(self, query: KnowledgeQuery) -> List[KnowledgeResult]:
        """Call Strands MCP (simulated)"""
        await asyncio.sleep(0.1)
        
        return [
            KnowledgeResult(
                content={
                    'name': f'Real-time Strands Template: {query.query_text}',
                    'description': 'This is a real-time Strands template...',
                    'template': '{"type": "realtime", "capabilities": []}',
                    'capabilities': ['realtime_capability']
                },
                source=DataSource.REALTIME,
                confidence_score=0.85,
                freshness=datetime.now(),
                metadata={'source_mcp': 'strands_mcp', 'realtime': True}
            )
        ]
    
    async def _call_github_mcp(self, query: KnowledgeQuery) -> List[KnowledgeResult]:
        """Call GitHub MCP (simulated)"""
        await asyncio.sleep(0.1)
        
        return [
            KnowledgeResult(
                content={
                    'name': f'realtime-mcp-{query.query_text.replace(" ", "-")}',
                    'description': f'Real-time MCP repository for {query.query_text}',
                    'stars': 100,
                    'language': 'Python',
                    'capabilities': ['realtime_search'],
                    'compatibility': {'agent_core': True}
                },
                source=DataSource.REALTIME,
                confidence_score=0.8,
                freshness=datetime.now(),
                metadata={'source_mcp': 'github_mcp', 'realtime': True}
            )
        ]
    
    def _matches_query(self, query_text: str, content: str) -> bool:
        """Simple text matching (in production, use more sophisticated search)"""
        query_words = query_text.lower().split()
        content_lower = content.lower()
        
        # Match if at least 50% of query words are found
        matches = sum(1 for word in query_words if word in content_lower)
        return matches >= len(query_words) * 0.5
    
    def _needs_realtime_fallback(self, results: List[KnowledgeResult], query: KnowledgeQuery) -> bool:
        """Determine if real-time fallback is needed"""
        if not results:
            return True
        
        # Check if results are too old
        now = datetime.now()
        for result in results:
            if now - result.freshness > self.freshness_threshold:
                return True
        
        # Check if confidence is too low
        avg_confidence = sum(r.confidence_score for r in results) / len(results)
        if avg_confidence < self.confidence_threshold:
            return True
        
        return False
    
    def _merge_results(self, cached_results: List[KnowledgeResult], 
                      realtime_results: List[KnowledgeResult], 
                      query: KnowledgeQuery) -> List[KnowledgeResult]:
        """Merge cached and real-time results intelligently"""
        merged = []
        
        # Prioritize real-time results for freshness-sensitive queries
        if query.query_type == QueryType.PRICING or query.freshness_required:
            merged.extend(realtime_results)
            merged.extend(cached_results)
        else:
            # Prioritize cached results for stability
            merged.extend(cached_results)
            merged.extend(realtime_results)
        
        # Remove duplicates and limit results
        seen = set()
        unique_results = []
        
        for result in merged:
            # Create a simple hash for deduplication
            content_hash = hashlib.md5(str(result.content).encode()).hexdigest()
            if content_hash not in seen:
                seen.add(content_hash)
                unique_results.append(result)
                
                if len(unique_results) >= query.max_results:
                    break
        
        return unique_results
    
    def _post_process_results(self, results: List[KnowledgeResult], 
                            query: KnowledgeQuery) -> List[KnowledgeResult]:
        """Post-process results for quality and relevance"""
        # Sort by confidence score and freshness
        results.sort(key=lambda r: (r.confidence_score, r.freshness), reverse=True)
        
        # Limit to max results
        return results[:query.max_results]
    
    def _record_query_metrics(self, query: KnowledgeQuery, 
                            results: List[KnowledgeResult], 
                            source: DataSource):
        """Record query metrics to CloudWatch"""
        try:
            self.cloudwatch.put_metric_data(
                Namespace=f'{self.project_name}/Knowledge-Access',
                MetricData=[
                    {
                        'MetricName': 'QueryCount',
                        'Dimensions': [
                            {'Name': 'QueryType', 'Value': query.query_type.value},
                            {'Name': 'DataSource', 'Value': source.value}
                        ],
                        'Value': 1,
                        'Unit': 'Count'
                    },
                    {
                        'MetricName': 'ResultCount',
                        'Dimensions': [
                            {'Name': 'QueryType', 'Value': query.query_type.value}
                        ],
                        'Value': len(results),
                        'Unit': 'Count'
                    }
                ]
            )
        except Exception as e:
            logger.error(f"Failed to record metrics: {str(e)}")

# Example usage
async def main():
    """Example usage of the hybrid knowledge access service"""
    service = HybridKnowledgeAccessService("agent-builder-platform", "dev")
    
    # Example queries
    queries = [
        KnowledgeQuery(
            query_text="EC2 pricing information",
            query_type=QueryType.PRICING,
            user_context={"experience_level": "beginner"}
        ),
        KnowledgeQuery(
            query_text="chatbot agent templates",
            query_type=QueryType.AGENT_TEMPLATES,
            user_context={"use_case": "customer_service"}
        ),
        KnowledgeQuery(
            query_text="filesystem MCP repositories",
            query_type=QueryType.MCP_REPOSITORIES,
            user_context={"integration_type": "agent_core"}
        )
    ]
    
    for query in queries:
        print(f"\nProcessing query: {query.query_text}")
        results = await service.query_knowledge(query)
        print(f"Found {len(results)} results")
        for i, result in enumerate(results[:2]):  # Show first 2 results
            print(f"  {i+1}. Source: {result.source.value}, Confidence: {result.confidence_score}")

if __name__ == "__main__":
    asyncio.run(main())