"""
MCP Health Monitoring and Fallback System
Monitors MCP availability, performance, and provides intelligent fallback mechanisms
"""

import json
import boto3
import logging
import asyncio
import aiohttp
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, asdict
from enum import Enum
import statistics

logger = logging.getLogger(__name__)

class MCPStatus(Enum):
    HEALTHY = "healthy"
    DEGRADED = "degraded"
    UNHEALTHY = "unhealthy"
    UNKNOWN = "unknown"

class FallbackStrategy(Enum):
    CACHED_ONLY = "cached_only"
    ALTERNATIVE_MCP = "alternative_mcp"
    GRACEFUL_DEGRADATION = "graceful_degradation"
    USER_NOTIFICATION = "user_notification"

@dataclass
class MCPHealthMetrics:
    mcp_name: str
    status: MCPStatus
    response_time: float
    success_rate: float
    last_check: datetime
    consecutive_failures: int
    error_message: Optional[str] = None

@dataclass
class FallbackAction:
    strategy: FallbackStrategy
    description: str
    estimated_impact: str
    user_message: str

class MCPHealthMonitor:
    """
    Comprehensive MCP health monitoring system that:
    - Continuously monitors MCP availability and performance
    - Implements intelligent fallback strategies
    - Provides user-friendly error handling
    - Maintains service reliability metrics
    """
    
    def __init__(self, project_name: str, environment: str):
        self.project_name = project_name
        self.environment = environment
        
        # AWS clients
        self.dynamodb = boto3.resource('dynamodb')
        self.cloudwatch = boto3.client('cloudwatch')
        self.sns = boto3.client('sns')
        
        # Health metrics table
        self.health_table = self.dynamodb.Table(f'{project_name}-mcp-health-{environment}')
        
        # Configuration
        self.health_check_interval = 300  # 5 minutes
        self.failure_threshold = 3  # consecutive failures before marking unhealthy
        self.response_time_threshold = 10.0  # seconds
        self.success_rate_threshold = 0.8  # 80%
        
        # MCP configurations
        self.mcp_configs = {
            'aws-docs': {
                'name': 'AWS Documentation MCP',
                'health_endpoint': 'http://localhost:4566/health',  # LocalStack for testing
                'timeout': 5,
                'critical': True,
                'fallback_mcps': ['cached-aws-docs']
            },
            'strands-mcp': {
                'name': 'Strands Agent Resources MCP',
                'health_endpoint': 'http://localhost:4567/health',
                'timeout': 5,
                'critical': True,
                'fallback_mcps': ['cached-strands']
            },
            'github-mcp': {
                'name': 'GitHub Repository Analysis MCP',
                'health_endpoint': 'http://localhost:4568/health',
                'timeout': 10,
                'critical': False,
                'fallback_mcps': ['cached-github']
            },
            'filesystem-mcp': {
                'name': 'Filesystem Operations MCP',
                'health_endpoint': 'http://localhost:4569/health',
                'timeout': 3,
                'critical': False,
                'fallback_mcps': []
            }
        }
        
        # Current health status cache
        self.health_cache: Dict[str, MCPHealthMetrics] = {}
        
        # Fallback strategies
        self.fallback_strategies = {
            'aws-docs': [
                FallbackAction(
                    strategy=FallbackStrategy.CACHED_ONLY,
                    description="Use cached AWS documentation",
                    estimated_impact="Slightly outdated information",
                    user_message="Using cached AWS documentation. Information may be slightly outdated."
                ),
                FallbackAction(
                    strategy=FallbackStrategy.GRACEFUL_DEGRADATION,
                    description="Provide basic AWS guidance without detailed docs",
                    estimated_impact="Reduced detail in AWS recommendations",
                    user_message="AWS documentation temporarily unavailable. Providing general guidance."
                )
            ],
            'strands-mcp': [
                FallbackAction(
                    strategy=FallbackStrategy.CACHED_ONLY,
                    description="Use cached Strands templates and examples",
                    estimated_impact="Limited to previously cached templates",
                    user_message="Using cached Strands resources. Some newer templates may not be available."
                ),
                FallbackAction(
                    strategy=FallbackStrategy.GRACEFUL_DEGRADATION,
                    description="Use basic agent templates without Strands integration",
                    estimated_impact="Simplified agent creation process",
                    user_message="Strands integration temporarily unavailable. Using basic agent templates."
                )
            ],
            'github-mcp': [
                FallbackAction(
                    strategy=FallbackStrategy.CACHED_ONLY,
                    description="Use cached MCP repository information",
                    estimated_impact="May miss newest MCP repositories",
                    user_message="Using cached MCP repository data. Newest repositories may not be shown."
                ),
                FallbackAction(
                    strategy=FallbackStrategy.GRACEFUL_DEGRADATION,
                    description="Skip MCP repository recommendations",
                    estimated_impact="No MCP discovery features",
                    user_message="MCP repository discovery temporarily unavailable."
                )
            ]
        }
    
    async def start_monitoring(self):
        """Start continuous health monitoring"""
        logger.info("Starting MCP health monitoring")
        
        while True:
            try:
                await self.check_all_mcps()
                await asyncio.sleep(self.health_check_interval)
            except Exception as e:
                logger.error(f"Health monitoring error: {str(e)}")
                await asyncio.sleep(60)  # Wait 1 minute before retrying
    
    async def check_all_mcps(self):
        """Check health of all configured MCPs"""
        logger.info("Performing health checks for all MCPs")
        
        # Create tasks for parallel health checks
        tasks = []
        for mcp_id, config in self.mcp_configs.items():
            task = asyncio.create_task(self.check_mcp_health(mcp_id, config))
            tasks.append(task)
        
        # Wait for all health checks to complete
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # Process results
        for i, result in enumerate(results):
            mcp_id = list(self.mcp_configs.keys())[i]
            
            if isinstance(result, Exception):
                logger.error(f"Health check failed for {mcp_id}: {str(result)}")
                await self.handle_health_check_failure(mcp_id, str(result))
            else:
                self.health_cache[mcp_id] = result
                await self.store_health_metrics(result)
                await self.evaluate_fallback_needs(mcp_id, result)
    
    async def check_mcp_health(self, mcp_id: str, config: Dict[str, Any]) -> MCPHealthMetrics:
        """Check health of a specific MCP"""
        start_time = datetime.now()
        
        try:
            # Perform health check
            async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=config['timeout'])) as session:
                async with session.get(config['health_endpoint']) as response:
                    response_time = (datetime.now() - start_time).total_seconds()
                    
                    if response.status == 200:
                        # Get previous metrics for success rate calculation
                        previous_metrics = self.health_cache.get(mcp_id)
                        success_rate = self._calculate_success_rate(mcp_id, True)
                        
                        status = MCPStatus.HEALTHY
                        if response_time > self.response_time_threshold:
                            status = MCPStatus.DEGRADED
                        
                        return MCPHealthMetrics(
                            mcp_name=config['name'],
                            status=status,
                            response_time=response_time,
                            success_rate=success_rate,
                            last_check=datetime.now(),
                            consecutive_failures=0
                        )
                    else:
                        raise Exception(f"HTTP {response.status}")
        
        except Exception as e:
            # Health check failed
            response_time = (datetime.now() - start_time).total_seconds()
            previous_metrics = self.health_cache.get(mcp_id)
            consecutive_failures = (previous_metrics.consecutive_failures + 1) if previous_metrics else 1
            success_rate = self._calculate_success_rate(mcp_id, False)
            
            status = MCPStatus.DEGRADED if consecutive_failures < self.failure_threshold else MCPStatus.UNHEALTHY
            
            return MCPHealthMetrics(
                mcp_name=config['name'],
                status=status,
                response_time=response_time,
                success_rate=success_rate,
                last_check=datetime.now(),
                consecutive_failures=consecutive_failures,
                error_message=str(e)
            )
    
    def _calculate_success_rate(self, mcp_id: str, current_success: bool) -> float:
        """Calculate success rate over recent checks"""
        # In production, this would query historical data from DynamoDB
        # For now, use a simple calculation
        previous_metrics = self.health_cache.get(mcp_id)
        
        if not previous_metrics:
            return 1.0 if current_success else 0.0
        
        # Simple moving average (in production, use more sophisticated calculation)
        weight = 0.1  # Weight for current check
        current_rate = 1.0 if current_success else 0.0
        return (1 - weight) * previous_metrics.success_rate + weight * current_rate
    
    async def handle_health_check_failure(self, mcp_id: str, error_message: str):
        """Handle health check failures"""
        logger.error(f"Health check failed for {mcp_id}: {error_message}")
        
        # Create failure metrics
        previous_metrics = self.health_cache.get(mcp_id)
        consecutive_failures = (previous_metrics.consecutive_failures + 1) if previous_metrics else 1
        
        failure_metrics = MCPHealthMetrics(
            mcp_name=self.mcp_configs[mcp_id]['name'],
            status=MCPStatus.UNKNOWN,
            response_time=0.0,
            success_rate=self._calculate_success_rate(mcp_id, False),
            last_check=datetime.now(),
            consecutive_failures=consecutive_failures,
            error_message=error_message
        )
        
        self.health_cache[mcp_id] = failure_metrics
        await self.store_health_metrics(failure_metrics)
        await self.evaluate_fallback_needs(mcp_id, failure_metrics)
    
    async def store_health_metrics(self, metrics: MCPHealthMetrics):
        """Store health metrics in DynamoDB"""
        try:
            # Store current metrics
            self.health_table.put_item(
                Item={
                    'mcp_name': metrics.mcp_name,
                    'timestamp': metrics.last_check.isoformat(),
                    'status': metrics.status.value,
                    'response_time': metrics.response_time,
                    'success_rate': metrics.success_rate,
                    'consecutive_failures': metrics.consecutive_failures,
                    'error_message': metrics.error_message,
                    'ttl': int((datetime.now() + timedelta(days=30)).timestamp())
                }
            )
            
            # Publish metrics to CloudWatch
            await self._publish_cloudwatch_metrics(metrics)
            
        except Exception as e:
            logger.error(f"Failed to store health metrics: {str(e)}")
    
    async def _publish_cloudwatch_metrics(self, metrics: MCPHealthMetrics):
        """Publish metrics to CloudWatch"""
        try:
            metric_data = [
                {
                    'MetricName': 'ResponseTime',
                    'Dimensions': [
                        {'Name': 'MCPName', 'Value': metrics.mcp_name}
                    ],
                    'Value': metrics.response_time,
                    'Unit': 'Seconds'
                },
                {
                    'MetricName': 'SuccessRate',
                    'Dimensions': [
                        {'Name': 'MCPName', 'Value': metrics.mcp_name}
                    ],
                    'Value': metrics.success_rate,
                    'Unit': 'Percent'
                },
                {
                    'MetricName': 'ConsecutiveFailures',
                    'Dimensions': [
                        {'Name': 'MCPName', 'Value': metrics.mcp_name}
                    ],
                    'Value': metrics.consecutive_failures,
                    'Unit': 'Count'
                }
            ]
            
            # Add status as binary metrics
            for status in MCPStatus:
                metric_data.append({
                    'MetricName': f'Status{status.value.title()}',
                    'Dimensions': [
                        {'Name': 'MCPName', 'Value': metrics.mcp_name}
                    ],
                    'Value': 1 if metrics.status == status else 0,
                    'Unit': 'Count'
                })
            
            self.cloudwatch.put_metric_data(
                Namespace=f'{self.project_name}/MCP-Health',
                MetricData=metric_data
            )
            
        except Exception as e:
            logger.error(f"Failed to publish CloudWatch metrics: {str(e)}")
    
    async def evaluate_fallback_needs(self, mcp_id: str, metrics: MCPHealthMetrics):
        """Evaluate if fallback strategies should be activated"""
        config = self.mcp_configs[mcp_id]
        
        # Check if MCP is critical and unhealthy
        if config['critical'] and metrics.status == MCPStatus.UNHEALTHY:
            await self._send_critical_alert(mcp_id, metrics)
        
        # Check if success rate is below threshold
        if metrics.success_rate < self.success_rate_threshold:
            await self._send_degradation_alert(mcp_id, metrics)
        
        # Log fallback recommendations
        if metrics.status in [MCPStatus.DEGRADED, MCPStatus.UNHEALTHY]:
            fallback_actions = self.fallback_strategies.get(mcp_id, [])
            if fallback_actions:
                logger.info(f"Fallback strategies available for {mcp_id}: {[a.strategy.value for a in fallback_actions]}")
    
    async def _send_critical_alert(self, mcp_id: str, metrics: MCPHealthMetrics):
        """Send critical alert for unhealthy critical MCP"""
        message = f"""
        CRITICAL: {metrics.mcp_name} is unhealthy
        
        Status: {metrics.status.value}
        Consecutive Failures: {metrics.consecutive_failures}
        Success Rate: {metrics.success_rate:.2%}
        Last Error: {metrics.error_message}
        
        Fallback strategies have been activated.
        """
        
        await self._send_sns_alert(f"CRITICAL: {metrics.mcp_name} Unhealthy", message)
    
    async def _send_degradation_alert(self, mcp_id: str, metrics: MCPHealthMetrics):
        """Send alert for degraded MCP performance"""
        message = f"""
        WARNING: {metrics.mcp_name} performance degraded
        
        Status: {metrics.status.value}
        Response Time: {metrics.response_time:.2f}s
        Success Rate: {metrics.success_rate:.2%}
        
        Monitoring for further degradation.
        """
        
        await self._send_sns_alert(f"WARNING: {metrics.mcp_name} Degraded", message)
    
    async def _send_sns_alert(self, subject: str, message: str):
        """Send SNS alert"""
        try:
            sns_topic_arn = f"arn:aws:sns:us-east-1:123456789012:{self.project_name}-alerts-{self.environment}"
            
            self.sns.publish(
                TopicArn=sns_topic_arn,
                Subject=subject,
                Message=message
            )
            
        except Exception as e:
            logger.error(f"Failed to send SNS alert: {str(e)}")
    
    def get_mcp_status(self, mcp_id: str) -> Optional[MCPHealthMetrics]:
        """Get current health status of an MCP"""
        return self.health_cache.get(mcp_id)
    
    def get_all_mcp_status(self) -> Dict[str, MCPHealthMetrics]:
        """Get health status of all MCPs"""
        return self.health_cache.copy()
    
    def get_fallback_actions(self, mcp_id: str) -> List[FallbackAction]:
        """Get available fallback actions for an MCP"""
        return self.fallback_strategies.get(mcp_id, [])
    
    def is_mcp_healthy(self, mcp_id: str) -> bool:
        """Check if an MCP is healthy"""
        metrics = self.health_cache.get(mcp_id)
        return metrics is not None and metrics.status == MCPStatus.HEALTHY
    
    def should_use_fallback(self, mcp_id: str) -> bool:
        """Determine if fallback should be used for an MCP"""
        metrics = self.health_cache.get(mcp_id)
        if not metrics:
            return True
        
        return metrics.status in [MCPStatus.DEGRADED, MCPStatus.UNHEALTHY]
    
    async def get_health_report(self) -> Dict[str, Any]:
        """Generate comprehensive health report"""
        report = {
            'timestamp': datetime.now().isoformat(),
            'overall_status': 'healthy',
            'mcps': {},
            'summary': {
                'total_mcps': len(self.mcp_configs),
                'healthy_mcps': 0,
                'degraded_mcps': 0,
                'unhealthy_mcps': 0,
                'critical_issues': []
            }
        }
        
        for mcp_id, config in self.mcp_configs.items():
            metrics = self.health_cache.get(mcp_id)
            
            if metrics:
                report['mcps'][mcp_id] = {
                    'name': metrics.mcp_name,
                    'status': metrics.status.value,
                    'response_time': metrics.response_time,
                    'success_rate': metrics.success_rate,
                    'last_check': metrics.last_check.isoformat(),
                    'consecutive_failures': metrics.consecutive_failures,
                    'error_message': metrics.error_message,
                    'is_critical': config['critical'],
                    'fallback_available': len(self.fallback_strategies.get(mcp_id, [])) > 0
                }
                
                # Update summary
                if metrics.status == MCPStatus.HEALTHY:
                    report['summary']['healthy_mcps'] += 1
                elif metrics.status == MCPStatus.DEGRADED:
                    report['summary']['degraded_mcps'] += 1
                else:
                    report['summary']['unhealthy_mcps'] += 1
                    
                    if config['critical']:
                        report['summary']['critical_issues'].append({
                            'mcp': mcp_id,
                            'issue': f"{metrics.mcp_name} is {metrics.status.value}"
                        })
            else:
                report['mcps'][mcp_id] = {
                    'name': config['name'],
                    'status': 'unknown',
                    'is_critical': config['critical']
                }
        
        # Determine overall status
        if report['summary']['critical_issues']:
            report['overall_status'] = 'critical'
        elif report['summary']['unhealthy_mcps'] > 0:
            report['overall_status'] = 'degraded'
        elif report['summary']['degraded_mcps'] > 0:
            report['overall_status'] = 'warning'
        
        return report

# Example usage and testing
async def main():
    """Example usage of MCP health monitoring"""
    monitor = MCPHealthMonitor("agent-builder-platform", "dev")
    
    # Perform one-time health check
    print("Performing health checks...")
    await monitor.check_all_mcps()
    
    # Get health report
    report = await monitor.get_health_report()
    print(f"\nHealth Report:")
    print(f"Overall Status: {report['overall_status']}")
    print(f"Healthy MCPs: {report['summary']['healthy_mcps']}")
    print(f"Degraded MCPs: {report['summary']['degraded_mcps']}")
    print(f"Unhealthy MCPs: {report['summary']['unhealthy_mcps']}")
    
    # Show individual MCP status
    for mcp_id, status in report['mcps'].items():
        print(f"  {status['name']}: {status['status']}")
        if status.get('error_message'):
            print(f"    Error: {status['error_message']}")
    
    # Show fallback strategies
    print(f"\nFallback Strategies:")
    for mcp_id in monitor.mcp_configs.keys():
        if monitor.should_use_fallback(mcp_id):
            actions = monitor.get_fallback_actions(mcp_id)
            print(f"  {mcp_id}: {len(actions)} fallback strategies available")
            for action in actions:
                print(f"    - {action.strategy.value}: {action.description}")

if __name__ == "__main__":
    asyncio.run(main())