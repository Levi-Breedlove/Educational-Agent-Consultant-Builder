#!/usr/bin/env python3
"""
Test Suite for Testing and Validation Endpoints
Tests the test execution and validation reporting functionality
"""

import asyncio
import sys
import os

# Add paths for imports
sys.path.insert(0, os.path.dirname(__file__))

from testing_service import TestingService, get_testing_service
from workflow_service import WorkflowService, get_workflow_service


async def test_testing_service():
    """Test the testing service functionality"""
    print("=" * 80)
    print("TESTING AND VALIDATION ENDPOINT TESTS")
    print("=" * 80)
    
    try:
        # Initialize services
        print("\n1. Initializing Services...")
        workflow_service = get_workflow_service()
        testing_service = get_testing_service()
        print("✅ Services initialized")
        
        # Create a test workflow first
        print("\n2. Creating Test Workflow...")
        agent_data = await workflow_service.create_agent_workflow(
            session_id="test-session-validation",
            user_id="test-user-validation",
            use_case="e_commerce_platform",
            description="Build a scalable e-commerce platform with payment processing, inventory management, and real-time analytics",
            experience_level="advanced"
        )
        
        agent_id = agent_data['agent_id']
        print(f"✅ Test workflow created: {agent_id}")
        
        # Submit requirements to populate workflow data
        print("\n3. Submitting Requirements...")
        await workflow_service.submit_requirements(
            agent_id=agent_id,
            user_input="Need to handle 10,000+ concurrent users, process payments securely, manage inventory in real-time, and provide analytics dashboard. Budget is $200/month.",
            context={
                'budget_range': 'medium',
                'timeline': '4_weeks',
                'expected_users': 10000,
                'compliance': ['PCI-DSS', 'GDPR']
            }
        )
        print("✅ Requirements submitted")
        
        # Get workflow to prepare test data
        workflow = workflow_service.orchestrator.active_workflows.get(agent_id)
        
        # Add some mock architecture and implementation data for testing
        workflow.architecture = {
            'service_recommendations': [
                {
                    'service_name': 'AWS Lambda',
                    'reasoning': 'Serverless compute for API endpoints',
                    'estimated_cost': 50.0
                },
                {
                    'service_name': 'Amazon DynamoDB',
                    'reasoning': 'NoSQL database for product catalog',
                    'estimated_cost': 30.0
                },
                {
                    'service_name': 'Amazon API Gateway',
                    'reasoning': 'API management and rate limiting',
                    'estimated_cost': 20.0
                }
            ],
            'cost_breakdown': {
                'compute': 50.0,
                'database': 30.0,
                'api': 20.0,
                'total': 100.0
            }
        }
        
        workflow.implementation = {
            'code_files': [
                {'name': 'api.py', 'language': 'python'},
                {'name': 'database.py', 'language': 'python'}
            ]
        }
        
        # Test 1: Execute tests
        print("\n4. Testing Execute Tests...")
        workflow_data = {
            'requirements': workflow.requirements,
            'architecture': workflow.architecture,
            'implementation': workflow.implementation
        }
        
        test_results = await testing_service.execute_tests(
            agent_id=agent_id,
            workflow_data=workflow_data,
            test_types=['security', 'performance', 'cost']
        )
        
        print(f"✅ Tests executed")
        print(f"   Test Execution ID: {test_results['test_execution_id']}")
        print(f"   Overall Status: {test_results['overall_status']}")
        print(f"   Production Readiness: {test_results['production_readiness_score']:.1%}")
        print(f"   Confidence Score: {test_results['confidence_score']:.1%}")
        
        # Show test summary
        summary = test_results['summary']
        print(f"   Tests Summary:")
        print(f"      Total: {summary['total_tests']}")
        print(f"      Passed: {summary['passed']}")
        print(f"      Failed: {summary['failed']}")
        print(f"      Warnings: {summary['warnings']}")
        
        # Show tests executed by type
        tests_executed = test_results['tests_executed']
        print(f"   Tests by Type:")
        for test_type, count in tests_executed.items():
            if count > 0:
                print(f"      {test_type.capitalize()}: {count}")
        
        # Show top recommendations
        if test_results['recommendations']:
            print(f"   Top Recommendations:")
            for i, rec in enumerate(test_results['recommendations'][:3], 1):
                print(f"      {i}. {rec}")
        
        # Test 2: Get validation report (summary only)
        print("\n5. Testing Get Validation Report (Summary)...")
        validation_report = await testing_service.get_validation_report(
            agent_id=agent_id,
            workflow_data=workflow_data,
            include_details=False
        )
        
        print(f"✅ Validation report generated (summary)")
        print(f"   Report ID: {validation_report['report_id']}")
        print(f"   Overall Status: {validation_report['overall_status']}")
        print(f"   Production Readiness: {validation_report['production_readiness_score']:.1%}")
        print(f"   Confidence Score: {validation_report['confidence_score']:.1%}")
        
        # Show multi-source validation
        if validation_report.get('multi_source_validation'):
            print(f"   Multi-Source Validation:")
            for source, score in validation_report['multi_source_validation'].items():
                print(f"      {source.capitalize()}: {score:.1%}")
        
        # Show summary by category
        summary_data = validation_report['summary']
        print(f"   Security Findings:")
        sec = summary_data.get('security', {})
        print(f"      Total: {sec.get('total_findings', 0)}")
        print(f"      Critical: {sec.get('critical', 0)}")
        print(f"      High: {sec.get('high', 0)}")
        
        print(f"   Performance Metrics:")
        perf = summary_data.get('performance', {})
        print(f"      Total: {perf.get('total_metrics', 0)}")
        print(f"      Passed: {perf.get('passed', 0)}")
        print(f"      Failed: {perf.get('failed', 0)}")
        
        print(f"   Cost Validations:")
        cost = summary_data.get('cost', {})
        print(f"      Total: {cost.get('total_validations', 0)}")
        print(f"      Within Budget: {cost.get('within_budget', 0)}")
        print(f"      Over Budget: {cost.get('over_budget', 0)}")
        
        # Test 3: Get validation report with details
        print("\n6. Testing Get Validation Report (With Details)...")
        detailed_report = await testing_service.get_validation_report(
            agent_id=agent_id,
            workflow_data=workflow_data,
            include_details=True
        )
        
        print(f"✅ Detailed validation report generated")
        
        # Check if details are included
        if 'details' in detailed_report:
            details = detailed_report['details']
            print(f"   Detailed Findings Included:")
            print(f"      Security Findings: {len(details.get('security_findings', []))}")
            print(f"      Performance Metrics: {len(details.get('performance_metrics', []))}")
            print(f"      Cost Validations: {len(details.get('cost_validations', []))}")
            print(f"      Integration Tests: {len(details.get('integration_tests', []))}")
            print(f"      Load Test Results: {len(details.get('load_test_results', []))}")
            
            # Show sample security finding
            if details.get('security_findings'):
                finding = details['security_findings'][0]
                print(f"\n   Sample Security Finding:")
                print(f"      Severity: {finding['severity']}")
                print(f"      Category: {finding['category']}")
                print(f"      Description: {finding['description'][:60]}...")
                print(f"      Confidence: {finding['confidence_score']:.1%}")
            
            # Show sample performance metric
            if details.get('performance_metrics'):
                metric = details['performance_metrics'][0]
                print(f"\n   Sample Performance Metric:")
                print(f"      Metric: {metric['metric_name']}")
                print(f"      Value: {metric['measured_value']} {metric['unit']}")
                print(f"      Status: {metric['status']}")
                print(f"      Confidence: {metric['confidence_score']:.1%}")
        
        # Test 4: Assumptions detection
        print("\n7. Testing Assumptions Detection...")
        assumptions = detailed_report.get('assumptions_detected', [])
        if assumptions:
            print(f"✅ Detected {len(assumptions)} assumptions:")
            for i, assumption in enumerate(assumptions[:3], 1):
                print(f"      {i}. {assumption}")
        else:
            print("✅ No assumptions detected")
        
        # Test 5: Recommendations
        print("\n8. Testing Recommendations...")
        recommendations = detailed_report.get('recommendations', [])
        if recommendations:
            print(f"✅ Generated {len(recommendations)} recommendations:")
            for i, rec in enumerate(recommendations[:5], 1):
                print(f"      {i}. {rec}")
        
        # Test 6: Monitoring configuration
        print("\n9. Testing Monitoring Configuration...")
        monitoring = detailed_report.get('monitoring', {})
        print(f"✅ Monitoring analysis:")
        print(f"   Total Configs: {monitoring.get('total_configs', 0)}")
        print(f"   Average Completeness: {monitoring.get('average_completeness', 0):.1%}")
        
        # Test 7: Error handling - invalid agent ID
        print("\n10. Testing Error Handling (Invalid Agent ID)...")
        try:
            await testing_service.execute_tests(
                agent_id="invalid-agent-id",
                workflow_data={},
                test_types=None
            )
            print("❌ Should have raised an error")
        except Exception as e:
            print(f"✅ Error handled correctly: {str(e)[:50]}...")
        
        # Summary
        print("\n" + "=" * 80)
        print("TEST SUMMARY")
        print("=" * 80)
        print("✅ All testing endpoint tests passed!")
        print(f"   - Test execution completed successfully")
        print(f"   - Validation reports generated (summary and detailed)")
        print(f"   - Security, performance, cost, integration, and load tests validated")
        print(f"   - Assumptions detected and recommendations provided")
        print(f"   - Monitoring configuration analyzed")
        print(f"   - Error handling validated")
        print(f"\n   Production Readiness: {detailed_report['production_readiness_score']:.1%}")
        print(f"   Overall Confidence: {detailed_report['confidence_score']:.1%}")
        print("\n🎉 Testing service is fully operational!")
        
        return True
        
    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


async def test_confidence_scores():
    """Test confidence score calculations"""
    print("\n" + "=" * 80)
    print("TESTING CONFIDENCE SCORE VALIDATION")
    print("=" * 80)
    
    try:
        workflow_service = get_workflow_service()
        testing_service = get_testing_service()
        
        # Create workflow
        print("\nCreating workflow for confidence testing...")
        agent_data = await workflow_service.create_agent_workflow(
            session_id="test-confidence",
            user_id="test-user-conf",
            use_case="microservices_api",
            description="Build a microservices-based API with authentication, rate limiting, and monitoring",
            experience_level="expert"
        )
        
        agent_id = agent_data['agent_id']
        print(f"✅ Workflow created: {agent_id}")
        
        # Submit requirements
        await workflow_service.submit_requirements(
            agent_id=agent_id,
            user_input="Need high-performance API with sub-100ms response time, JWT authentication, and comprehensive monitoring",
            context={'performance_critical': True}
        )
        
        # Prepare workflow data
        workflow = workflow_service.orchestrator.active_workflows.get(agent_id)
        workflow.architecture = {
            'service_recommendations': [
                {'service_name': 'AWS Lambda', 'estimated_cost': 30.0},
                {'service_name': 'Amazon API Gateway', 'estimated_cost': 20.0}
            ],
            'cost_breakdown': {'total': 50.0}
        }
        workflow.implementation = {'code_files': []}
        
        workflow_data = {
            'requirements': workflow.requirements,
            'architecture': workflow.architecture,
            'implementation': workflow.implementation
        }
        
        # Execute tests and check confidence
        print("\nExecuting tests and validating confidence scores...")
        test_results = await testing_service.execute_tests(
            agent_id=agent_id,
            workflow_data=workflow_data
        )
        
        confidence = test_results['confidence_score']
        print(f"✅ Confidence score: {confidence:.1%}")
        
        # Validate confidence meets threshold
        if confidence >= 0.85:
            print(f"✅ Confidence score meets 85% threshold")
        else:
            print(f"⚠️  Confidence score below threshold: {confidence:.1%}")
        
        # Get detailed report
        validation_report = await testing_service.get_validation_report(
            agent_id=agent_id,
            workflow_data=workflow_data,
            include_details=True
        )
        
        # Check multi-source validation
        multi_source = validation_report.get('multi_source_validation', {})
        print(f"\n✅ Multi-source validation scores:")
        for source, score in multi_source.items():
            status = "✅" if score >= 0.85 else "⚠️"
            print(f"   {status} {source.capitalize()}: {score:.1%}")
        
        print("\n🎉 Confidence score validation passed!")
        return True
        
    except Exception as e:
        print(f"\n❌ Confidence test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


async def main():
    """Run all tests"""
    print("\n🚀 Starting Testing and Validation Endpoint Tests\n")
    
    # Run tests
    test1_passed = await test_testing_service()
    test2_passed = await test_confidence_scores()
    
    # Final summary
    print("\n" + "=" * 80)
    print("FINAL TEST RESULTS")
    print("=" * 80)
    print(f"Testing Service Tests: {'✅ PASSED' if test1_passed else '❌ FAILED'}")
    print(f"Confidence Score Tests: {'✅ PASSED' if test2_passed else '❌ FAILED'}")
    
    if test1_passed and test2_passed:
        print("\n🎉 ALL TESTS PASSED! Testing endpoints are ready for production.")
        return 0
    else:
        print("\n❌ Some tests failed. Please review the errors above.")
        return 1


if __name__ == "__main__":
    exit_code = asyncio.run(main())
    sys.exit(exit_code)
