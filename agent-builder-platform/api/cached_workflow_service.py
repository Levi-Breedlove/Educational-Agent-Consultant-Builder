#!/usr/bin/env python3
"""
Cached Workflow Service
Wraps workflow service with performance optimizations
"""

import asyncio
from typing import Dict, Any, List, Optional
import logging

from .workflow_service import WorkflowService, get_workflow_service
from .performance_service import get_performance_service, cached

logger = logging.getLogger(__name__)


class CachedWorkflowService:
    """
    Workflow service with caching and performance optimizations
    """
    
    def __init__(self, workflow_service: WorkflowService):
        self.workflow_service = workflow_service
        self.performance_service = get_performance_service()
    
    async def create_agent_workflow(
        self,
        session_id: str,
        user_id: Optional[str],
        use_case: str,
        description: str,
        experience_level: str
    ) -> Dict[str, Any]:
        """Create agent workflow (not cached - always fresh)"""
        return await self.workflow_service.create_agent_workflow(
            session_id=session_id,
            user_id=user_id,
            use_case=use_case,
            description=description,
            experience_level=experience_level
        )
    
    async def submit_requirements(
        self,
        agent_id: str,
        user_input: str,
        context: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Submit requirements with caching for similar queries
        """
        # Use caching for requirements analysis
        async def analyze_requirements():
            return await self.workflow_service.submit_requirements(
                agent_id=agent_id,
                user_input=user_input,
                context=context
            )
        
        # Cache based on user input (similar requirements get cached results)
        return await self.performance_service.cached_call(
            analyze_requirements,
            f"requirements:{agent_id}",
            ttl_seconds=600,  # 10 minutes
        )
    
    async def process_feedback(
        self,
        agent_id: str,
        feedback_type: str,
        content: str,
        rating: Optional[int] = None
    ) -> Dict[str, Any]:
        """Process feedback (not cached - always fresh)"""
        return await self.workflow_service.process_feedback(
            agent_id=agent_id,
            feedback_type=feedback_type,
            content=content,
            rating=rating
        )
    
    async def get_workflow_status(self, agent_id: str) -> Dict[str, Any]:
        """
        Get workflow status with short-term caching
        """
        async def fetch_status():
            return await self.workflow_service.get_workflow_status(agent_id)
        
        # Short cache for status (5 seconds)
        return await self.performance_service.cached_call(
            fetch_status,
            f"status:{agent_id}",
            ttl_seconds=5
        )
    
    async def get_recommendations(
        self,
        agent_id: str,
        recommendation_type: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Get recommendations with caching
        """
        async def fetch_recommendations():
            return await self.workflow_service.get_recommendations(
                agent_id=agent_id,
                recommendation_type=recommendation_type
            )
        
        # Cache recommendations for 5 minutes
        return await self.performance_service.cached_call(
            fetch_recommendations,
            f"recommendations:{agent_id}:{recommendation_type}",
            ttl_seconds=300
        )
    
    async def parallel_mcp_queries(
        self,
        queries: List[Dict[str, Any]],
        max_concurrent: int = 5
    ) -> List[Any]:
        """
        Execute multiple MCP queries in parallel
        
        Args:
            queries: List of query dictionaries with 'mcp' and 'query' keys
            max_concurrent: Maximum concurrent queries
        
        Returns:
            List of query results
        """
        async def execute_query(query_data: Dict[str, Any]):
            mcp_name = query_data.get('mcp')
            query_text = query_data.get('query')
            
            # Simulate MCP query (replace with actual MCP integration)
            logger.info(f"Executing MCP query: {mcp_name} - {query_text}")
            await asyncio.sleep(0.1)  # Simulate network delay
            
            return {
                'mcp': mcp_name,
                'query': query_text,
                'result': f"Result from {mcp_name}",
                'confidence': 0.95
            }
        
        # Create tasks for parallel execution
        tasks = [lambda q=q: execute_query(q) for q in queries]
        
        # Execute in parallel with concurrency limit
        results = await self.performance_service.parallel_execute(
            tasks,
            max_concurrent=max_concurrent
        )
        
        return results


# Singleton instance
_cached_workflow_service: Optional[CachedWorkflowService] = None


def get_cached_workflow_service() -> CachedWorkflowService:
    """Get or create cached workflow service singleton"""
    global _cached_workflow_service
    if _cached_workflow_service is None:
        workflow_service = get_workflow_service()
        _cached_workflow_service = CachedWorkflowService(workflow_service)
    return _cached_workflow_service
