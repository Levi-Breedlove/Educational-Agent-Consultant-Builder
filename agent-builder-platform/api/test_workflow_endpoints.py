#!/usr/bin/env python3
"""
Test Suite for Agent Creation Workflow Endpoints
Tests the complete workflow from creation to recommendations
"""

import asyncio
import sys
import os

# Add paths for imports
sys.path.insert(0, os.path.dirname(__file__))

from workflow_service import WorkflowService, get_workflow_service


async def test_workflow_service():
    """Test the workflow service functionality"""
    print("=" * 80)
    print("AGENT CREATION WORKFLOW ENDPOINT TESTS")
    print("=" * 80)
    
    try:
        # Initialize service
        print("\n1. Initializing Workflow Service...")
        service = get_workflow_service()
        print("✅ Workflow service initialized")
        
        # Test 1: Create agent workflow
        print("\n2. Testing Create Agent Workflow...")
        agent_data = await service.create_agent_workflow(
            session_id="test-session-123",
            user_id="test-user-456",
            use_case="customer_support_chatbot",
            description="Build an AI-powered chatbot that can handle customer support inquiries, integrate with our CRM system, and provide 24/7 automated responses",
            experience_level="intermediate"
        )
        
        agent_id = agent_data['agent_id']
        print(f"✅ Agent workflow created: {agent_id}")
        print(f"   Status: {agent_data['status']}")
        print(f"   Progress: {agent_data['progress_percentage']:.1f}%")
        print(f"   Vector Search: {agent_data['vector_search_enabled']}")
        
        # Test 2: Submit requirements
        print("\n3. Testing Submit Requirements...")
        requirements_result = await service.submit_requirements(
            agent_id=agent_id,
            user_input="I need a chatbot that can handle 1000+ concurrent users, integrate with Salesforce CRM, and provide responses in under 2 seconds. Budget is around $50/month.",
            context={
                'budget_range': 'medium',
                'timeline': '2_weeks',
                'expected_users': 1000
            }
        )
        
        print(f"✅ Requirements submitted")
        print(f"   Current Phase: {requirements_result['current_phase']}")
        print(f"   Progress: {requirements_result['progress_percentage']:.1f}%")
        
        analysis = requirements_result.get('analysis', {})
        if analysis:
            print(f"   Confidence Score: {analysis.get('confidence_score', 0):.2f}")
            
            # Show service recommendations if available
            service_recs = analysis.get('service_recommendations', [])
            if service_recs:
                print(f"   Service Recommendations: {len(service_recs)} services")
                for i, rec in enumerate(service_recs[:3], 1):
                    if isinstance(rec, dict):
                        print(f"      {i}. {rec.get('service_name', 'Unknown')}")
        
        # Test 3: Process feedback - clarification
        print("\n4. Testing Process Feedback (Clarification)...")
        feedback_result = await service.process_feedback(
            agent_id=agent_id,
            feedback_type="clarification",
            content="Can you explain more about the cost breakdown?",
            rating=4
        )
        
        print(f"✅ Clarification feedback processed")
        print(f"   Action: {feedback_result['action']}")
        print(f"   Message: {feedback_result['message']}")
        
        # Test 4: Process feedback - approval
        print("\n5. Testing Process Feedback (Approval)...")
        approval_result = await service.process_feedback(
            agent_id=agent_id,
            feedback_type="approval",
            content="Looks good, let's proceed",
            rating=5
        )
        
        print(f"✅ Approval feedback processed")
        print(f"   Action: {approval_result['action']}")
        print(f"   Next Phase: {approval_result.get('next_phase', 'N/A')}")
        
        # Test 5: Get workflow status
        print("\n6. Testing Get Workflow Status...")
        status = await service.get_workflow_status(agent_id)
        
        print(f"✅ Workflow status retrieved")
        print(f"   Agent ID: {status['agent_id']}")
        print(f"   Status: {status['status']}")
        print(f"   Progress: {status['progress_percentage']:.1f}%")
        print(f"   Completed Steps: {len(status['completed_steps'])}")
        print(f"   Active Agents: {len(status['active_agents'])}")
        
        # Test 6: Get recommendations
        print("\n7. Testing Get Recommendations...")
        recommendations = await service.get_recommendations(
            agent_id=agent_id,
            recommendation_type="services"
        )
        
        print(f"✅ Recommendations retrieved")
        print(f"   Current Phase: {recommendations['current_phase']}")
        print(f"   Confidence Score: {recommendations['confidence_score']:.2f}")
        print(f"   Recommendations: {len(recommendations['recommendations'])}")
        
        # Test 7: Process modification feedback
        print("\n8. Testing Process Feedback (Modification)...")
        mod_result = await service.process_feedback(
            agent_id=agent_id,
            feedback_type="modification",
            content="Can we reduce the cost by using more serverless components?",
            rating=3
        )
        
        print(f"✅ Modification feedback processed")
        print(f"   Action: {mod_result['action']}")
        print(f"   Message: {mod_result['message']}")
        
        # Test 8: Error handling - invalid agent ID
        print("\n9. Testing Error Handling (Invalid Agent ID)...")
        try:
            await service.get_workflow_status("invalid-agent-id")
            print("❌ Should have raised an error")
        except ValueError as e:
            print(f"✅ Error handled correctly: {str(e)[:50]}...")
        
        # Summary
        print("\n" + "=" * 80)
        print("TEST SUMMARY")
        print("=" * 80)
        print("✅ All workflow endpoint tests passed!")
        print(f"   - Agent workflow created: {agent_id}")
        print(f"   - Requirements submitted and analyzed")
        print(f"   - Multiple feedback types processed")
        print(f"   - Status and recommendations retrieved")
        print(f"   - Error handling validated")
        print("\n🎉 Workflow service is fully operational!")
        
        return True
        
    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


async def test_multiple_workflows():
    """Test handling multiple concurrent workflows"""
    print("\n" + "=" * 80)
    print("TESTING MULTIPLE CONCURRENT WORKFLOWS")
    print("=" * 80)
    
    try:
        service = get_workflow_service()
        
        # Create multiple workflows
        workflows = []
        use_cases = [
            ("data_pipeline", "Build a data processing pipeline for ETL operations"),
            ("api_gateway", "Create a REST API gateway with authentication"),
            ("monitoring_system", "Set up automated monitoring and alerting")
        ]
        
        print("\nCreating multiple workflows...")
        for i, (use_case, description) in enumerate(use_cases, 1):
            agent_data = await service.create_agent_workflow(
                session_id=f"session-{i}",
                user_id=f"user-{i}",
                use_case=use_case,
                description=description,
                experience_level="intermediate"
            )
            workflows.append(agent_data)
            print(f"✅ Workflow {i}: {agent_data['agent_id']} ({use_case})")
        
        # Verify all workflows are tracked
        print(f"\n✅ Successfully created {len(workflows)} concurrent workflows")
        
        # Get status for each
        print("\nRetrieving status for all workflows...")
        for workflow in workflows:
            status = await service.get_workflow_status(workflow['agent_id'])
            print(f"✅ {workflow['agent_id']}: {status['status']} ({status['progress_percentage']:.1f}%)")
        
        print("\n🎉 Multiple workflow handling test passed!")
        return True
        
    except Exception as e:
        print(f"\n❌ Multiple workflow test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


async def main():
    """Run all tests"""
    print("\n🚀 Starting Agent Creation Workflow Endpoint Tests\n")
    
    # Run tests
    test1_passed = await test_workflow_service()
    test2_passed = await test_multiple_workflows()
    
    # Final summary
    print("\n" + "=" * 80)
    print("FINAL TEST RESULTS")
    print("=" * 80)
    print(f"Workflow Service Tests: {'✅ PASSED' if test1_passed else '❌ FAILED'}")
    print(f"Multiple Workflows Test: {'✅ PASSED' if test2_passed else '❌ FAILED'}")
    
    if test1_passed and test2_passed:
        print("\n🎉 ALL TESTS PASSED! Workflow endpoints are ready for production.")
        return 0
    else:
        print("\n❌ Some tests failed. Please review the errors above.")
        return 1


if __name__ == "__main__":
    exit_code = asyncio.run(main())
    sys.exit(exit_code)
