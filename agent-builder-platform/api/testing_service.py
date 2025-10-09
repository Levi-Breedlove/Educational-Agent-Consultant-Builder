#!/usr/bin/env python3
"""
Testing and Validation Service
Manages test execution and validation reporting
"""

import logging
import sys
import os
from typing import Dict, Any, Optional, List
from datetime import datetime

# Add paths for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'agents'))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'agent-core'))

from testing_validator import TestingValidator, ValidationReport, ValidationStatus

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class TestingService:
    """Service for managing testing and validation"""
    
    def __init__(self):
        """Initialize testing service with validator agent"""
        self.validator = TestingValidator()
        logger.info("Testing service initialized")
    
    async def execute_tests(
        self,
        agent_id: str,
        workflow_data: Dict[str, Any],
        test_types: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """
        Execute tests for an agent implementation
        
        Args:
            agent_id: Agent/project identifier
            workflow_data: Complete workflow data (requirements, architecture, implementation)
            test_types: Optional list of specific test types to run
            
        Returns:
            Test execution results
        """
        try:
            logger.info(f"Executing tests for agent: {agent_id}")
            
            # Extract workflow components
            requirements = workflow_data.get('requirements', {})
            architecture = workflow_data.get('architecture', {})
            implementation = workflow_data.get('implementation', {})
            
            # Run comprehensive validation
            validation_report = await self.validator.validate_implementation(
                implementation=implementation,
                architecture=architecture,
                requirements=requirements,
                user_context={'agent_id': agent_id}
            )
            
            # Format test results
            test_results = {
                'agent_id': agent_id,
                'test_execution_id': validation_report.report_id,
                'timestamp': validation_report.timestamp.isoformat(),
                'overall_status': validation_report.overall_status.value,
                'tests_executed': {
                    'security': len(validation_report.security_findings),
                    'performance': len(validation_report.performance_metrics),
                    'cost': len(validation_report.cost_validations),
                    'integration': len(validation_report.integration_tests),
                    'load': len(validation_report.load_test_results)
                },
                'summary': {
                    'total_tests': (
                        len(validation_report.security_findings) +
                        len(validation_report.performance_metrics) +
                        len(validation_report.cost_validations) +
                        len(validation_report.integration_tests) +
                        len(validation_report.load_test_results)
                    ),
                    'passed': self._count_passed_tests(validation_report),
                    'failed': self._count_failed_tests(validation_report),
                    'warnings': self._count_warnings(validation_report)
                },
                'production_readiness_score': validation_report.production_readiness_score,
                'confidence_score': validation_report.confidence_score,
                'recommendations': validation_report.recommendations[:5]  # Top 5
            }
            
            logger.info(f"Tests executed for agent: {agent_id}, status: {validation_report.overall_status.value}")
            
            return test_results
            
        except Exception as e:
            logger.error(f"Failed to execute tests: {e}")
            raise
    
    async def get_validation_report(
        self,
        agent_id: str,
        workflow_data: Dict[str, Any],
        include_details: bool = True
    ) -> Dict[str, Any]:
        """
        Get comprehensive validation report
        
        Args:
            agent_id: Agent/project identifier
            workflow_data: Complete workflow data
            include_details: Whether to include detailed findings
            
        Returns:
            Comprehensive validation report
        """
        try:
            logger.info(f"Generating validation report for agent: {agent_id}")
            
            # Extract workflow components
            requirements = workflow_data.get('requirements', {})
            architecture = workflow_data.get('architecture', {})
            implementation = workflow_data.get('implementation', {})
            
            # Run validation
            validation_report = await self.validator.validate_implementation(
                implementation=implementation,
                architecture=architecture,
                requirements=requirements,
                user_context={'agent_id': agent_id}
            )
            
            # Build comprehensive report
            report = {
                'agent_id': agent_id,
                'report_id': validation_report.report_id,
                'timestamp': validation_report.timestamp.isoformat(),
                'overall_status': validation_report.overall_status.value,
                'production_readiness_score': validation_report.production_readiness_score,
                'confidence_score': validation_report.confidence_score,
                'multi_source_validation': validation_report.multi_source_validation,
                'summary': {
                    'security': {
                        'total_findings': len(validation_report.security_findings),
                        'critical': self._count_by_severity(validation_report.security_findings, 'critical'),
                        'high': self._count_by_severity(validation_report.security_findings, 'high'),
                        'medium': self._count_by_severity(validation_report.security_findings, 'medium'),
                        'low': self._count_by_severity(validation_report.security_findings, 'low')
                    },
                    'performance': {
                        'total_metrics': len(validation_report.performance_metrics),
                        'passed': self._count_by_status(validation_report.performance_metrics, 'passed'),
                        'failed': self._count_by_status(validation_report.performance_metrics, 'failed'),
                        'warnings': self._count_by_status(validation_report.performance_metrics, 'warning')
                    },
                    'cost': {
                        'total_validations': len(validation_report.cost_validations),
                        'within_budget': self._count_by_status(validation_report.cost_validations, 'passed'),
                        'over_budget': self._count_by_status(validation_report.cost_validations, 'failed')
                    },
                    'integration': {
                        'total_tests': len(validation_report.integration_tests),
                        'passed': self._count_by_status(validation_report.integration_tests, 'passed'),
                        'failed': self._count_by_status(validation_report.integration_tests, 'failed')
                    },
                    'load': {
                        'total_scenarios': len(validation_report.load_test_results),
                        'passed': self._count_by_status(validation_report.load_test_results, 'passed'),
                        'failed': self._count_by_status(validation_report.load_test_results, 'failed')
                    }
                },
                'assumptions_detected': validation_report.assumptions_detected,
                'recommendations': validation_report.recommendations,
                'monitoring': {
                    'total_configs': len(validation_report.monitoring_configs),
                    'average_completeness': self._calculate_avg_completeness(validation_report.monitoring_configs)
                }
            }
            
            # Add detailed findings if requested
            if include_details:
                report['details'] = {
                    'security_findings': [
                        {
                            'finding_id': f.finding_id,
                            'severity': f.severity.value,
                            'category': f.category,
                            'description': f.description,
                            'affected_resource': f.affected_resource,
                            'remediation': f.remediation,
                            'confidence_score': f.confidence_score
                        }
                        for f in validation_report.security_findings
                    ],
                    'performance_metrics': [
                        {
                            'metric_name': m.metric_name,
                            'measured_value': m.measured_value,
                            'unit': m.unit,
                            'threshold_value': m.threshold_value,
                            'status': m.status.value,
                            'recommendations': m.optimization_recommendations,
                            'confidence_score': m.confidence_score
                        }
                        for m in validation_report.performance_metrics
                    ],
                    'cost_validations': [
                        {
                            'service_name': c.service_name,
                            'estimated_cost': c.estimated_cost,
                            'actual_projected_cost': c.actual_projected_cost,
                            'variance_percentage': c.variance_percentage,
                            'status': c.status.value,
                            'optimization_opportunities': c.optimization_opportunities,
                            'confidence_score': c.confidence_score
                        }
                        for c in validation_report.cost_validations
                    ],
                    'integration_tests': [
                        {
                            'test_name': t.test_name,
                            'service_name': t.service_name,
                            'status': t.status.value,
                            'execution_time_ms': t.execution_time_ms,
                            'error_message': t.error_message,
                            'recommendations': t.recommendations,
                            'confidence_score': t.confidence_score
                        }
                        for t in validation_report.integration_tests
                    ],
                    'load_test_results': [
                        {
                            'test_scenario': l.test_scenario,
                            'concurrent_users': l.concurrent_users,
                            'requests_per_second': l.requests_per_second,
                            'average_response_time_ms': l.average_response_time_ms,
                            'p95_response_time_ms': l.p95_response_time_ms,
                            'error_rate_percentage': l.error_rate_percentage,
                            'status': l.throughput_status.value,
                            'bottlenecks': l.bottlenecks,
                            'recommendations': l.recommendations,
                            'confidence_score': l.confidence_score
                        }
                        for l in validation_report.load_test_results
                    ]
                }
            
            logger.info(f"Validation report generated for agent: {agent_id}")
            
            return report
            
        except Exception as e:
            logger.error(f"Failed to generate validation report: {e}")
            raise
    
    def _count_passed_tests(self, report: ValidationReport) -> int:
        """Count total passed tests"""
        passed = 0
        passed += self._count_by_status(report.performance_metrics, 'passed')
        passed += self._count_by_status(report.cost_validations, 'passed')
        passed += self._count_by_status(report.integration_tests, 'passed')
        passed += self._count_by_status(report.load_test_results, 'passed')
        return passed
    
    def _count_failed_tests(self, report: ValidationReport) -> int:
        """Count total failed tests"""
        failed = 0
        failed += self._count_by_status(report.performance_metrics, 'failed')
        failed += self._count_by_status(report.cost_validations, 'failed')
        failed += self._count_by_status(report.integration_tests, 'failed')
        failed += self._count_by_status(report.load_test_results, 'failed')
        return failed
    
    def _count_warnings(self, report: ValidationReport) -> int:
        """Count total warnings"""
        warnings = 0
        warnings += self._count_by_status(report.performance_metrics, 'warning')
        warnings += self._count_by_status(report.cost_validations, 'warning')
        warnings += self._count_by_status(report.integration_tests, 'warning')
        warnings += self._count_by_status(report.load_test_results, 'warning')
        return warnings
    
    def _count_by_severity(self, findings: List, severity: str) -> int:
        """Count findings by severity level"""
        return sum(1 for f in findings if f.severity.value == severity)
    
    def _count_by_status(self, items: List, status: str) -> int:
        """Count items by status"""
        count = 0
        for item in items:
            if hasattr(item, 'status') and item.status.value == status:
                count += 1
            elif hasattr(item, 'throughput_status') and item.throughput_status.value == status:
                count += 1
        return count
    
    def _calculate_avg_completeness(self, configs: List) -> float:
        """Calculate average monitoring completeness"""
        if not configs:
            return 0.0
        return sum(c.completeness_score for c in configs) / len(configs)


# Singleton instance
_testing_service: Optional[TestingService] = None


def get_testing_service() -> TestingService:
    """Get testing service instance (singleton)"""
    global _testing_service
    if _testing_service is None:
        _testing_service = TestingService()
    return _testing_service
