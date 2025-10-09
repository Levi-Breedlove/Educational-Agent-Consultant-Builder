"""
Agent Core MCP Integration Wrapper
Integrates the hybrid knowledge access system with Agent Core framework
"""

import json
import logging
import asyncio
from typing import Dict, List, Any, Optional, Union
from datetime import datetime
import os

# Agent Core imports (these would be actual imports in production)
# from agent_core import Agent, Tool, Context, Message
# from agent_core.mcp import MCPClient

from enhanced_knowledge_service import (
    EnhancedKnowledgeAccessService, 
    KnowledgeQuery, 
    QueryType, 
    KnowledgeResult
)
from mcp_health_monitor import MCPHealthMonitor

logger = logging.getLogger(__name__)

class AgentCoreMCPWrapper:
    """
    Wrapper that integrates our hybrid MCP system with Agent Core framework.
    Provides Agent Core agents with reliable access to knowledge through
    both cached data and real-time MCP calls.
    """
    
    def __init__(self, project_name: str, environment: str):
        self.project_name = project_name
        self.environment = environment
        
        # Initialize our enhanced hybrid knowledge system with vector search
        self.knowledge_service = EnhancedKnowledgeAccessService(
            project_name, 
            environment,
            enable_vector_search=True
        )
        self.health_monitor = MCPHealthMonitor(project_name, environment)
        
        # Agent Core integration
        self.agent_core_tools = self._create_agent_core_tools()
        
        # Start health monitoring in background
        asyncio.create_task(self.health_monitor.start_monitoring())
    
    def _create_agent_core_tools(self) -> Dict[str, Any]:
        """Create Agent Core tools for MCP integration"""
        return {
            'aws_documentation_search': {
                'name': 'aws_documentation_search',
                'description': 'Search AWS documentation with intelligent caching and real-time fallback',
                'parameters': {
                    'type': 'object',
                    'properties': {
                        'query': {
                            'type': 'string',
                            'description': 'Search query for AWS documentation'
                        },
                        'service': {
                            'type': 'string',
                            'description': 'Specific AWS service to search (optional)'
                        },
                        'freshness_required': {
                            'type': 'boolean',
                            'description': 'Whether real-time data is required',
                            'default': False
                        }
                    },
                    'required': ['query']
                },
                'function': self.search_aws_documentation
            },
            'strands_template_search': {
                'name': 'strands_template_search',
                'description': 'Search Strands agent templates and capabilities',
                'parameters': {
                    'type': 'object',
                    'properties': {
                        'query': {
                            'type': 'string',
                            'description': 'Search query for Strands templates'
                        },
                        'capability_type': {
                            'type': 'string',
                            'description': 'Type of capability needed (optional)'
                        }
                    },
                    'required': ['query']
                },
                'function': self.search_strands_templates
            },
            'mcp_repository_search': {
                'name': 'mcp_repository_search',
                'description': 'Search and analyze MCP repositories for recommendations',
                'parameters': {
                    'type': 'object',
                    'properties': {
                        'query': {
                            'type': 'string',
                            'description': 'Search query for MCP repositories'
                        },
                        'use_case': {
                            'type': 'string',
                            'description': 'Specific use case for MCP selection'
                        },
                        'compatibility': {
                            'type': 'string',
                            'description': 'Required compatibility (agent_core, strands, etc.)'
                        }
                    },
                    'required': ['query']
                },
                'function': self.search_mcp_repositories
            },
            'get_mcp_health_status': {
                'name': 'get_mcp_health_status',
                'description': 'Get current health status of MCP services',
                'parameters': {
                    'type': 'object',
                    'properties': {
                        'mcp_name': {
                            'type': 'string',
                            'description': 'Specific MCP to check (optional, returns all if not specified)'
                        }
                    }
                },
                'function': self.get_mcp_health_status
            },
            'get_knowledge_recommendations': {
                'name': 'get_knowledge_recommendations',
                'description': 'Get intelligent recommendations based on user context and requirements',
                'parameters': {
                    'type': 'object',
                    'properties': {
                        'user_requirements': {
                            'type': 'string',
                            'description': 'User requirements description'
                        },
                        'experience_level': {
                            'type': 'string',
                            'description': 'User experience level (beginner, intermediate, advanced)'
                        },
                        'use_case': {
                            'type': 'string',
                            'description': 'Specific use case or domain'
                        }
                    },
                    'required': ['user_requirements']
                },
                'function': self.get_knowledge_recommendations
            }
        }
    
    async def search_aws_documentation(self, query: str, service: Optional[str] = None, 
                                     freshness_required: bool = False, 
                                     user_context: Optional[Dict] = None) -> Dict[str, Any]:
        """Search AWS documentation with intelligent routing"""
        try:
            # Create knowledge query
            knowledge_query = KnowledgeQuery(
                query_text=f"{service} {query}" if service else query,
                query_type=QueryType.DOCUMENTATION,
                user_context=user_context or {},
                max_results=5,
                freshness_required=freshness_required
            )
            
            # Execute search
            results = await self.knowledge_service.query_knowledge(knowledge_query)
            
            # Format results for Agent Core
            formatted_results = []
            for result in results:
                formatted_results.append({
                    'title': result.content.get('title', 'AWS Documentation'),
                    'content': result.content.get('content', ''),
                    'url': result.content.get('url', ''),
                    'source': result.source.value,
                    'confidence': result.confidence_score,
                    'freshness': result.freshness.isoformat(),
                    'relevant_service': service
                })
            
            return {
                'success': True,
                'results': formatted_results,
                'total_results': len(formatted_results),
                'query_info': {
                    'original_query': query,
                    'service_filter': service,
                    'freshness_required': freshness_required
                },
                'data_sources_used': list(set(r['source'] for r in formatted_results))
            }
            
        except Exception as e:
            logger.error(f"AWS documentation search failed: {str(e)}")
            return {
                'success': False,
                'error': str(e),
                'fallback_message': 'AWS documentation search temporarily unavailable. Please try again or use cached results.'
            }
    
    async def search_strands_templates(self, query: str, capability_type: Optional[str] = None,
                                     user_context: Optional[Dict] = None) -> Dict[str, Any]:
        """Search Strands agent templates and capabilities"""
        try:
            # Determine query type based on what user is looking for
            query_type = QueryType.AGENT_TEMPLATES
            if capability_type or 'capability' in query.lower():
                query_type = QueryType.CAPABILITIES
            
            knowledge_query = KnowledgeQuery(
                query_text=f"{capability_type} {query}" if capability_type else query,
                query_type=query_type,
                user_context=user_context or {},
                max_results=10
            )
            
            results = await self.knowledge_service.query_knowledge(knowledge_query)
            
            formatted_results = []
            for result in results:
                formatted_results.append({
                    'name': result.content.get('name', 'Strands Template'),
                    'description': result.content.get('description', ''),
                    'template': result.content.get('template', ''),
                    'capabilities': result.content.get('capabilities', []),
                    'examples': result.content.get('examples', []),
                    'source': result.source.value,
                    'confidence': result.confidence_score,
                    'freshness': result.freshness.isoformat()
                })
            
            return {
                'success': True,
                'results': formatted_results,
                'total_results': len(formatted_results),
                'query_info': {
                    'original_query': query,
                    'capability_type': capability_type,
                    'query_type': query_type.value
                },
                'recommendations': self._generate_strands_recommendations(formatted_results, user_context)
            }
            
        except Exception as e:
            logger.error(f"Strands template search failed: {str(e)}")
            return {
                'success': False,
                'error': str(e),
                'fallback_message': 'Strands template search temporarily unavailable. Using basic templates.'
            }
    
    async def search_mcp_repositories(self, query: str, use_case: Optional[str] = None,
                                    compatibility: Optional[str] = None,
                                    user_context: Optional[Dict] = None) -> Dict[str, Any]:
        """Search and analyze MCP repositories"""
        try:
            knowledge_query = KnowledgeQuery(
                query_text=f"{use_case} {query}" if use_case else query,
                query_type=QueryType.MCP_REPOSITORIES,
                user_context=user_context or {},
                max_results=15
            )
            
            results = await self.knowledge_service.query_knowledge(knowledge_query)
            
            # Filter by compatibility if specified
            if compatibility:
                filtered_results = []
                for result in results:
                    repo_compatibility = result.content.get('compatibility', {})
                    if repo_compatibility.get(compatibility, False):
                        filtered_results.append(result)
                results = filtered_results
            
            formatted_results = []
            for result in results:
                formatted_results.append({
                    'name': result.content.get('name', 'MCP Repository'),
                    'description': result.content.get('description', ''),
                    'stars': result.content.get('stars', 0),
                    'language': result.content.get('language', ''),
                    'capabilities': result.content.get('capabilities', []),
                    'compatibility': result.content.get('compatibility', {}),
                    'usage_examples': result.content.get('usage_examples', []),
                    'source': result.source.value,
                    'confidence': result.confidence_score,
                    'recommendation_score': self._calculate_mcp_recommendation_score(result, use_case, compatibility)
                })
            
            # Sort by recommendation score
            formatted_results.sort(key=lambda x: x['recommendation_score'], reverse=True)
            
            return {
                'success': True,
                'results': formatted_results,
                'total_results': len(formatted_results),
                'query_info': {
                    'original_query': query,
                    'use_case': use_case,
                    'compatibility_filter': compatibility
                },
                'recommendations': self._generate_mcp_recommendations(formatted_results, use_case, compatibility)
            }
            
        except Exception as e:
            logger.error(f"MCP repository search failed: {str(e)}")
            return {
                'success': False,
                'error': str(e),
                'fallback_message': 'MCP repository search temporarily unavailable. Using cached recommendations.'
            }
    
    async def get_mcp_health_status(self, mcp_name: Optional[str] = None) -> Dict[str, Any]:
        """Get MCP health status"""
        try:
            if mcp_name:
                # Get specific MCP status
                status = self.health_monitor.get_mcp_status(mcp_name)
                if status:
                    return {
                        'success': True,
                        'mcp_name': mcp_name,
                        'status': status.status.value,
                        'response_time': status.response_time,
                        'success_rate': status.success_rate,
                        'last_check': status.last_check.isoformat(),
                        'consecutive_failures': status.consecutive_failures,
                        'error_message': status.error_message,
                        'fallback_available': len(self.health_monitor.get_fallback_actions(mcp_name)) > 0
                    }
                else:
                    return {
                        'success': False,
                        'error': f'MCP {mcp_name} not found'
                    }
            else:
                # Get all MCP status
                health_report = await self.health_monitor.get_health_report()
                return {
                    'success': True,
                    'overall_status': health_report['overall_status'],
                    'summary': health_report['summary'],
                    'mcps': health_report['mcps'],
                    'timestamp': health_report['timestamp']
                }
                
        except Exception as e:
            logger.error(f"Health status check failed: {str(e)}")
            return {
                'success': False,
                'error': str(e)
            }
    
    async def get_knowledge_recommendations(self, user_requirements: str, 
                                          experience_level: str = 'intermediate',
                                          use_case: Optional[str] = None,
                                          user_context: Optional[Dict] = None) -> Dict[str, Any]:
        """Get intelligent recommendations based on user context"""
        try:
            recommendations = {
                'aws_services': [],
                'strands_templates': [],
                'mcp_integrations': [],
                'architecture_patterns': [],
                'cost_considerations': [],
                'security_recommendations': []
            }
            
            # Analyze user requirements to determine what they need
            context = user_context or {}
            context.update({
                'experience_level': experience_level,
                'use_case': use_case,
                'requirements': user_requirements
            })
            
            # Search for relevant AWS services
            aws_query = KnowledgeQuery(
                query_text=user_requirements,
                query_type=QueryType.DOCUMENTATION,
                user_context=context,
                max_results=3
            )
            aws_results = await self.knowledge_service.query_knowledge(aws_query)
            
            for result in aws_results:
                recommendations['aws_services'].append({
                    'service': result.content.get('title', ''),
                    'description': result.content.get('content', '')[:200] + '...',
                    'confidence': result.confidence_score,
                    'why_recommended': self._explain_aws_recommendation(result, context)
                })
            
            # Search for relevant Strands templates
            strands_query = KnowledgeQuery(
                query_text=user_requirements,
                query_type=QueryType.AGENT_TEMPLATES,
                user_context=context,
                max_results=3
            )
            strands_results = await self.knowledge_service.query_knowledge(strands_query)
            
            for result in strands_results:
                recommendations['strands_templates'].append({
                    'name': result.content.get('name', ''),
                    'description': result.content.get('description', ''),
                    'capabilities': result.content.get('capabilities', []),
                    'confidence': result.confidence_score,
                    'why_recommended': self._explain_strands_recommendation(result, context)
                })
            
            # Search for relevant MCPs
            mcp_query = KnowledgeQuery(
                query_text=user_requirements,
                query_type=QueryType.MCP_REPOSITORIES,
                user_context=context,
                max_results=5
            )
            mcp_results = await self.knowledge_service.query_knowledge(mcp_query)
            
            for result in mcp_results:
                recommendations['mcp_integrations'].append({
                    'name': result.content.get('name', ''),
                    'description': result.content.get('description', ''),
                    'capabilities': result.content.get('capabilities', []),
                    'compatibility': result.content.get('compatibility', {}),
                    'confidence': result.confidence_score,
                    'why_recommended': self._explain_mcp_recommendation(result, context)
                })
            
            # Generate architecture and cost recommendations
            recommendations['architecture_patterns'] = self._generate_architecture_recommendations(context)
            recommendations['cost_considerations'] = self._generate_cost_recommendations(context)
            recommendations['security_recommendations'] = self._generate_security_recommendations(context)
            
            return {
                'success': True,
                'recommendations': recommendations,
                'user_context': {
                    'requirements': user_requirements,
                    'experience_level': experience_level,
                    'use_case': use_case
                },
                'confidence_score': self._calculate_overall_confidence(recommendations),
                'next_steps': self._generate_next_steps(recommendations, context)
            }
            
        except Exception as e:
            logger.error(f"Knowledge recommendations failed: {str(e)}")
            return {
                'success': False,
                'error': str(e),
                'fallback_message': 'Unable to generate recommendations. Please try with more specific requirements.'
            }
    
    def _generate_strands_recommendations(self, results: List[Dict], user_context: Optional[Dict]) -> List[str]:
        """Generate recommendations based on Strands search results"""
        recommendations = []
        
        if not results:
            recommendations.append("No specific Strands templates found. Consider using basic agent templates.")
            return recommendations
        
        # Analyze results and generate recommendations
        high_confidence_results = [r for r in results if r['confidence'] > 0.8]
        if high_confidence_results:
            recommendations.append(f"Found {len(high_confidence_results)} highly relevant templates")
        
        # Check for specific capabilities
        all_capabilities = []
        for result in results:
            all_capabilities.extend(result.get('capabilities', []))
        
        unique_capabilities = list(set(all_capabilities))
        if unique_capabilities:
            recommendations.append(f"Available capabilities: {', '.join(unique_capabilities[:5])}")
        
        return recommendations
    
    def _calculate_mcp_recommendation_score(self, result: KnowledgeResult, 
                                          use_case: Optional[str], 
                                          compatibility: Optional[str]) -> float:
        """Calculate recommendation score for MCP repository"""
        score = result.confidence_score
        
        # Boost score for high star count
        stars = result.content.get('stars', 0)
        if stars > 100:
            score += 0.1
        elif stars > 50:
            score += 0.05
        
        # Boost score for compatibility match
        if compatibility:
            repo_compatibility = result.content.get('compatibility', {})
            if repo_compatibility.get(compatibility, False):
                score += 0.2
        
        # Boost score for use case relevance
        if use_case:
            description = result.content.get('description', '').lower()
            if use_case.lower() in description:
                score += 0.15
        
        return min(score, 1.0)  # Cap at 1.0
    
    def _generate_mcp_recommendations(self, results: List[Dict], 
                                    use_case: Optional[str], 
                                    compatibility: Optional[str]) -> List[str]:
        """Generate MCP recommendations"""
        recommendations = []
        
        if not results:
            recommendations.append("No specific MCPs found for your requirements. Consider basic filesystem or web search MCPs.")
            return recommendations
        
        # Top recommendations
        top_results = results[:3]
        recommendations.append(f"Top recommendation: {top_results[0]['name']} - {top_results[0]['description']}")
        
        # Compatibility analysis
        if compatibility:
            compatible_count = sum(1 for r in results if r['compatibility'].get(compatibility, False))
            recommendations.append(f"{compatible_count} MCPs are compatible with {compatibility}")
        
        return recommendations
    
    def _explain_aws_recommendation(self, result: KnowledgeResult, context: Dict) -> str:
        """Explain why an AWS service is recommended"""
        service_name = result.content.get('title', 'AWS Service')
        experience = context.get('experience_level', 'intermediate')
        
        if experience == 'beginner':
            return f"{service_name} is recommended because it's well-documented and beginner-friendly"
        elif experience == 'advanced':
            return f"{service_name} offers advanced features suitable for complex use cases"
        else:
            return f"{service_name} provides good balance of features and ease of use"
    
    def _explain_strands_recommendation(self, result: KnowledgeResult, context: Dict) -> str:
        """Explain why a Strands template is recommended"""
        template_name = result.content.get('name', 'Template')
        capabilities = result.content.get('capabilities', [])
        
        if capabilities:
            return f"{template_name} provides {', '.join(capabilities[:2])} capabilities needed for your use case"
        else:
            return f"{template_name} is a good starting point for your requirements"
    
    def _explain_mcp_recommendation(self, result: KnowledgeResult, context: Dict) -> str:
        """Explain why an MCP is recommended"""
        mcp_name = result.content.get('name', 'MCP')
        capabilities = result.content.get('capabilities', [])
        stars = result.content.get('stars', 0)
        
        reasons = []
        if stars > 100:
            reasons.append("highly popular")
        if capabilities:
            reasons.append(f"provides {', '.join(capabilities[:2])}")
        
        if reasons:
            return f"{mcp_name} is recommended because it's {' and '.join(reasons)}"
        else:
            return f"{mcp_name} matches your requirements"
    
    def _generate_architecture_recommendations(self, context: Dict) -> List[str]:
        """Generate architecture pattern recommendations"""
        recommendations = []
        experience = context.get('experience_level', 'intermediate')
        use_case = context.get('use_case', '')
        
        if experience == 'beginner':
            recommendations.append("Start with a simple single-service architecture")
            recommendations.append("Use managed services to reduce operational complexity")
        else:
            recommendations.append("Consider microservices architecture for scalability")
            recommendations.append("Implement proper monitoring and observability")
        
        if 'data' in use_case.lower():
            recommendations.append("Consider data pipeline architecture with S3 and Lambda")
        
        return recommendations
    
    def _generate_cost_recommendations(self, context: Dict) -> List[str]:
        """Generate cost optimization recommendations"""
        recommendations = [
            "Leverage AWS free tier for development and testing",
            "Use spot instances for non-critical workloads",
            "Implement auto-scaling to optimize resource usage",
            "Monitor costs with CloudWatch billing alerts"
        ]
        
        experience = context.get('experience_level', 'intermediate')
        if experience == 'beginner':
            recommendations.insert(0, "Start with pay-as-you-go pricing to minimize upfront costs")
        
        return recommendations
    
    def _generate_security_recommendations(self, context: Dict) -> List[str]:
        """Generate security recommendations"""
        return [
            "Use IAM roles with least privilege principle",
            "Enable encryption at rest and in transit",
            "Implement proper VPC security groups",
            "Enable CloudTrail for audit logging",
            "Use AWS Secrets Manager for sensitive data"
        ]
    
    def _calculate_overall_confidence(self, recommendations: Dict) -> float:
        """Calculate overall confidence score for recommendations"""
        total_items = 0
        total_confidence = 0.0
        
        for category, items in recommendations.items():
            if isinstance(items, list) and items:
                for item in items:
                    if isinstance(item, dict) and 'confidence' in item:
                        total_confidence += item['confidence']
                        total_items += 1
        
        return total_confidence / total_items if total_items > 0 else 0.8
    
    def _generate_next_steps(self, recommendations: Dict, context: Dict) -> List[str]:
        """Generate next steps based on recommendations"""
        steps = []
        
        if recommendations['aws_services']:
            steps.append("Review recommended AWS services and their pricing")
        
        if recommendations['strands_templates']:
            steps.append("Examine Strands templates and select the most suitable one")
        
        if recommendations['mcp_integrations']:
            steps.append("Configure recommended MCP integrations")
        
        steps.extend([
            "Create a proof of concept with selected components",
            "Set up monitoring and cost tracking",
            "Plan for production deployment"
        ])
        
        return steps
    
    def get_agent_core_tools(self) -> Dict[str, Any]:
        """Get tools for Agent Core integration"""
        return self.agent_core_tools
    
    async def initialize_for_agent_core(self) -> Dict[str, Any]:
        """Initialize the wrapper for Agent Core integration"""
        try:
            # Perform initial health check
            health_status = await self.get_mcp_health_status()
            
            return {
                'success': True,
                'tools_available': list(self.agent_core_tools.keys()),
                'mcp_health': health_status,
                'capabilities': [
                    'AWS documentation search with caching',
                    'Strands template and capability search',
                    'MCP repository analysis and recommendations',
                    'Intelligent knowledge routing',
                    'Health monitoring and fallback strategies'
                ]
            }
            
        except Exception as e:
            logger.error(f"Agent Core initialization failed: {str(e)}")
            return {
                'success': False,
                'error': str(e),
                'fallback_mode': True
            }

# Example usage for testing
async def main():
    """Example usage of the Agent Core MCP wrapper"""
    wrapper = AgentCoreMCPWrapper("agent-builder-platform", "dev")
    
    # Initialize
    init_result = await wrapper.initialize_for_agent_core()
    print(f"Initialization: {init_result['success']}")
    
    # Test AWS documentation search
    aws_result = await wrapper.search_aws_documentation(
        query="EC2 instance types",
        service="EC2",
        user_context={"experience_level": "beginner"}
    )
    print(f"AWS search results: {len(aws_result.get('results', []))}")
    
    # Test knowledge recommendations
    recommendations = await wrapper.get_knowledge_recommendations(
        user_requirements="I need to build a chatbot that can answer customer questions",
        experience_level="intermediate",
        use_case="customer_service"
    )
    print(f"Recommendations generated: {recommendations['success']}")

if __name__ == "__main__":
    asyncio.run(main())