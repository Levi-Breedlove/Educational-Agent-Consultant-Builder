#!/usr/bin/env python3
"""
MCP Health Monitor
Monitors health and availability of all 16 MCPs in the ecosystem
"""

import json
import boto3
import logging
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from datetime import datetime, timedelta
from enum import Enum
import asyncio

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class HealthStatus(Enum):
    """Health status levels"""
    HEALTHY = "healthy"
    DEGRADED = "degraded"
    UNHEALTHY = "unhealthy"
    UNKNOWN = "unknown"

@dataclass
class MCPHealthStatus:
    """Health status for a single MCP"""
    mcp_type: str
    status: HealthStatus
    last_check: datetime
    response_time: Optional[float] = None
    error_message: Optional[str] = None
    consecutive_failures: int = 0
    uptime_percentage: float = 100.0
    metadata: Dict[str, Any] = None

    def __post_init__(self):
        if self.metadata is None:
            self.metadata = {}

class MCPHealthMonitor:
    """Monitors health of all MCPs in the ecosystem"""
    
    def __init__(self, project_name: str, environment: str = "dev"):
        self.project_name = project_name
        self.environment = environment
        
        # Initialize AWS clients
        self.dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
        self.cloudwatch = boto3.client('cloudwatch', region_name='us-east-1')
        
        # Health metrics table
        self.health_table_name = f"{project_name}-health-metrics-{environment}"
        
        # Health status cache
        self.health_cache: Dict[str, MCPHealthStatus] = {}
        
        # Health check configuration
        self.health_check_interval = 300  # 5 minutes
        self.failure_threshold = 3  # Consecutive failures before marking unhealthy
        self.response_timeout = 30  # seconds
        
        # MCP endpoints for health checks (simulated for demo)
        self.mcp_endpoints = {
            'aws_documentation': 'https://api.aws-docs-mcp.example.com/health',
            'aws_well_architected': 'https://api.aws-wa-mcp.example.com/health',
            'aws_solutions': 'https://api.aws-solutions-mcp.example.com/health',
            'aws_security': 'https://api.aws-security-mcp.example.com/health',
            'aws_serverless': 'https://api.aws-serverless-mcp.example.com/health',
            'aws_containers': 'https://api.aws-containers-mcp.example.com/health',
            'aws_ai_ml': 'https://api.aws-aiml-mcp.example.com/health',
            'aws_pricing': 'https://api.aws-pricing-mcp.example.com/health',
            'aws_devops': 'https://api.aws-devops-mcp.example.com/health',
            'aws_monitoring': 'https://api.aws-monitoring-mcp.example.com/health',
            'aws_networking': 'https://api.aws-networking-mcp.example.com/health',
            'aws_agent_core_patterns': 'https://api.aws-patterns-mcp.example.com/health',
            'github_analysis': 'https://api.github-analysis-mcp.example.com/health',
            'perplexity_research': 'https://api.perplexity-research-mcp.example.com/health',
            'strands_patterns': 'https://api.strands-patterns-mcp.example.com/health',
            'filesystem': 'https://api.filesystem-mcp.example.com/health'
        }
        
        # Initialize health table
        self._initialize_health_table()
        
        logger.info(f"MCP Health Monitor initialized for {len(self.mcp_endpoints)} MCPs")

    def _initialize_health_table(self):
        """Initialize DynamoDB table for health metrics"""
        try:
            self.health_table = self.dynamodb.Table(self.health_table_name)
            logger.info(f"Health metrics table initialized: {self.health_table_name}")
        except Exception as e:
            logger.error(f"Failed to initialize health table: {e}")
            raise

    async def check_mcp_health(self, mcp_type: str) -> MCPHealthStatus:
        """Check health of a specific MCP"""
        try:
            start_time = datetime.utcnow()
            
            # Get endpoint for health check
            endpoint = self.mcp_endpoints.get(mcp_type)
            if not endpoint:
                return MCPHealthStatus(
                    mcp_type=mcp_type,
                    status=HealthStatus.UNKNOWN,
                    last_check=start_time,
                    error_message="No endpoint configured"
                )
            
            # Simulate health check (in production, this would make actual HTTP calls)
            health_status = await self._simulate_health_check(mcp_type, endpoint)
            
            # Calculate response time
            response_time = (datetime.utcnow() - start_time).total_seconds()
            health_status.response_time = response_time
            health_status.last_check = start_time
            
            # Update cache
            self.health_cache[mcp_type] = health_status
            
            # Store in DynamoDB
            await self._store_health_metrics(health_status)
            
            # Send CloudWatch metrics
            await self._send_cloudwatch_metrics(health_status)
            
            return health_status
            
        except Exception as e:
            logger.error(f"Health check failed for {mcp_type}: {e}")
            
            # Get previous status for consecutive failure tracking
            previous_status = self.health_cache.get(mcp_type)
            consecutive_failures = (previous_status.consecutive_failures + 1) if previous_status else 1
            
            error_status = MCPHealthStatus(
                mcp_type=mcp_type,
                status=HealthStatus.UNHEALTHY,
                last_check=datetime.utcnow(),
                error_message=str(e),
                consecutive_failures=consecutive_failures
            )
            
            self.health_cache[mcp_type] = error_status
            return error_status

    async def _simulate_health_check(self, mcp_type: str, endpoint: str) -> MCPHealthStatus:
        """Simulate MCP health check (replace with actual HTTP calls in production)"""
        # Simulate different health scenarios for demo
        import random
        
        # Most MCPs are healthy most of the time
        health_probability = 0.9
        
        # Some MCPs have different reliability patterns
        if mcp_type in ['perplexity_research', 'github_analysis']:
            health_probability = 0.85  # External services slightly less reliable
        elif mcp_type.startswith('aws_'):
            health_probability = 0.95  # AWS services very reliable
        
        is_healthy = random.random() < health_probability
        
        if is_healthy:
            return MCPHealthStatus(
                mcp_type=mcp_type,
                status=HealthStatus.HEALTHY,
                last_check=datetime.utcnow(),
                consecutive_failures=0,
                metadata={'endpoint': endpoint, 'simulated': True}
            )
        else:
            # Simulate different types of failures
            failure_types = [
                ("Connection timeout", HealthStatus.UNHEALTHY),
                ("Rate limit exceeded", HealthStatus.DEGRADED),
                ("Service unavailable", HealthStatus.UNHEALTHY),
                ("Authentication failed", HealthStatus.DEGRADED)
            ]
            
            error_message, status = random.choice(failure_types)
            
            return MCPHealthStatus(
                mcp_type=mcp_type,
                status=status,
                last_check=datetime.utcnow(),
                error_message=error_message,
                consecutive_failures=1,
                metadata={'endpoint': endpoint, 'simulated': True}
            )

    async def _store_health_metrics(self, health_status: MCPHealthStatus):
        """Store health metrics in DynamoDB"""
        try:
            item = {
                'mcp_type': health_status.mcp_type,
                'timestamp': health_status.last_check.isoformat(),
                'status': health_status.status.value,
                'response_time': health_status.response_time,
                'consecutive_failures': health_status.consecutive_failures,
                'error_message': health_status.error_message,
                'metadata': health_status.metadata or {}
            }
            
            self.health_table.put_item(Item=item)
            logger.debug(f"Stored health metrics for {health_status.mcp_type}")
            
        except Exception as e:
            logger.error(f"Failed to store health metrics: {e}")

    async def _send_cloudwatch_metrics(self, health_status: MCPHealthStatus):
        """Send health metrics to CloudWatch"""
        try:
            # Convert status to numeric value for CloudWatch
            status_value = {
                HealthStatus.HEALTHY: 1,
                HealthStatus.DEGRADED: 0.5,
                HealthStatus.UNHEALTHY: 0,
                HealthStatus.UNKNOWN: -1
            }.get(health_status.status, -1)
            
            # Send metrics
            self.cloudwatch.put_metric_data(
                Namespace=f'AgentBuilder/{self.project_name}',
                MetricData=[
                    {
                        'MetricName': 'MCPHealth',
                        'Dimensions': [
                            {
                                'Name': 'MCPType',
                                'Value': health_status.mcp_type
                            },
                            {
                                'Name': 'Environment',
                                'Value': self.environment
                            }
                        ],
                        'Value': status_value,
                        'Unit': 'None',
                        'Timestamp': health_status.last_check
                    }
                ]
            )
            
            # Send response time metric if available
            if health_status.response_time is not None:
                self.cloudwatch.put_metric_data(
                    Namespace=f'AgentBuilder/{self.project_name}',
                    MetricData=[
                        {
                            'MetricName': 'MCPResponseTime',
                            'Dimensions': [
                                {
                                    'Name': 'MCPType',
                                    'Value': health_status.mcp_type
                                }
                            ],
                            'Value': health_status.response_time,
                            'Unit': 'Seconds',
                            'Timestamp': health_status.last_check
                        }
                    ]
                )
            
            logger.debug(f"Sent CloudWatch metrics for {health_status.mcp_type}")
            
        except Exception as e:
            logger.error(f"Failed to send CloudWatch metrics: {e}")

    async def check_all_mcps_health(self) -> Dict[str, MCPHealthStatus]:
        """Check health of all MCPs in parallel"""
        logger.info("Starting health check for all MCPs")
        
        # Create tasks for parallel health checks
        tasks = []
        for mcp_type in self.mcp_endpoints.keys():
            task = asyncio.create_task(self.check_mcp_health(mcp_type))
            tasks.append((mcp_type, task))
        
        # Wait for all health checks to complete
        results = {}
        for mcp_type, task in tasks:
            try:
                health_status = await task
                results[mcp_type] = health_status
            except Exception as e:
                logger.error(f"Health check task failed for {mcp_type}: {e}")
                results[mcp_type] = MCPHealthStatus(
                    mcp_type=mcp_type,
                    status=HealthStatus.UNKNOWN,
                    last_check=datetime.utcnow(),
                    error_message=str(e)
                )
        
        # Log summary
        healthy_count = sum(1 for status in results.values() if status.status == HealthStatus.HEALTHY)
        degraded_count = sum(1 for status in results.values() if status.status == HealthStatus.DEGRADED)
        unhealthy_count = sum(1 for status in results.values() if status.status == HealthStatus.UNHEALTHY)
        
        logger.info(f"Health check completed: {healthy_count} healthy, {degraded_count} degraded, {unhealthy_count} unhealthy")
        
        return results

    def is_mcp_healthy(self, mcp_type: str) -> bool:
        """Check if an MCP is currently healthy"""
        health_status = self.health_cache.get(mcp_type)
        
        if not health_status:
            # No cached status, assume healthy but trigger health check
            logger.warning(f"No cached health status for {mcp_type}, assuming healthy")
            return True
        
        # Check if status is recent (within 2x health check interval)
        age = datetime.utcnow() - health_status.last_check
        if age.total_seconds() > (self.health_check_interval * 2):
            logger.warning(f"Stale health status for {mcp_type}, assuming healthy")
            return True
        
        return health_status.status in [HealthStatus.HEALTHY, HealthStatus.DEGRADED]

    def get_mcp_status(self, mcp_type: str) -> Optional[MCPHealthStatus]:
        """Get current health status for an MCP"""
        return self.health_cache.get(mcp_type)

    def get_ecosystem_health_summary(self) -> Dict[str, Any]:
        """Get overall ecosystem health summary"""
        if not self.health_cache:
            return {
                'overall_status': 'unknown',
                'total_mcps': len(self.mcp_endpoints),
                'healthy': 0,
                'degraded': 0,
                'unhealthy': 0,
                'unknown': len(self.mcp_endpoints)
            }
        
        healthy = sum(1 for status in self.health_cache.values() if status.status == HealthStatus.HEALTHY)
        degraded = sum(1 for status in self.health_cache.values() if status.status == HealthStatus.DEGRADED)
        unhealthy = sum(1 for status in self.health_cache.values() if status.status == HealthStatus.UNHEALTHY)
        unknown = len(self.mcp_endpoints) - len(self.health_cache)
        
        # Determine overall status
        if unhealthy > 0:
            overall_status = 'critical'
        elif degraded > 0:
            overall_status = 'degraded'
        elif healthy == len(self.mcp_endpoints):
            overall_status = 'healthy'
        else:
            overall_status = 'warning'
        
        return {
            'overall_status': overall_status,
            'total_mcps': len(self.mcp_endpoints),
            'healthy': healthy,
            'degraded': degraded,
            'unhealthy': unhealthy,
            'unknown': unknown,
            'uptime_percentage': (healthy + degraded) / len(self.mcp_endpoints) * 100 if self.mcp_endpoints else 0
        }

    async def start_continuous_monitoring(self):
        """Start continuous health monitoring"""
        logger.info("Starting continuous MCP health monitoring")
        
        while True:
            try:
                await self.check_all_mcps_health()
                await asyncio.sleep(self.health_check_interval)
            except Exception as e:
                logger.error(f"Error in continuous monitoring: {e}")
                await asyncio.sleep(60)  # Wait 1 minute before retrying

# Test function
async def test_mcp_health_monitor():
    """Test the MCP health monitor"""
    print("🚀 Testing MCP Health Monitor...")
    
    monitor = MCPHealthMonitor("agent-builder-platform", "test")
    
    # Test individual health check
    print("\n--- Testing Individual Health Check ---")
    health_status = await monitor.check_mcp_health('aws_documentation')
    print(f"✅ AWS Documentation MCP: {health_status.status.value}")
    print(f"   Response time: {health_status.response_time:.3f}s")
    
    # Test all MCPs health check
    print("\n--- Testing All MCPs Health Check ---")
    all_health = await monitor.check_all_mcps_health()
    
    for mcp_type, status in all_health.items():
        status_icon = "✅" if status.status == HealthStatus.HEALTHY else "⚠️" if status.status == HealthStatus.DEGRADED else "❌"
        print(f"{status_icon} {mcp_type}: {status.status.value}")
    
    # Test ecosystem summary
    print("\n--- Testing Ecosystem Health Summary ---")
    summary = monitor.get_ecosystem_health_summary()
    print(f"✅ Overall status: {summary['overall_status']}")
    print(f"   Healthy: {summary['healthy']}/{summary['total_mcps']}")
    print(f"   Degraded: {summary['degraded']}/{summary['total_mcps']}")
    print(f"   Unhealthy: {summary['unhealthy']}/{summary['total_mcps']}")
    print(f"   Uptime: {summary['uptime_percentage']:.1f}%")
    
    print("\n🎉 MCP Health Monitor test completed!")
    return True

if __name__ == "__main__":
    asyncio.run(test_mcp_health_monitor())