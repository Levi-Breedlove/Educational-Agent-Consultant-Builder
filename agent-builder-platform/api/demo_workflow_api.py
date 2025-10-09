#!/usr/bin/env python3
"""
Demo Script for Agent Creation Workflow API
Shows how to use the workflow endpoints in a real scenario
"""

import asyncio
import sys
import os

sys.path.insert(0, os.path.dirname(__file__))

from workflow_service import get_workflow_service
from session_service import get_session_service


async def demo_complete_workflow():
    """
    Demonstrate a complete agent creation workflow
    Simulates a user creating a customer support chatbot
    """
    print("=" * 80)
    print("AGENT CREATION WORKFLOW API DEMO")
    print("Scenario: Building a Customer Support Chatbot")
    print("=" * 80)
    
    # Initialize services
    session_service = get_session_service()
    workflow_service = get_workflow_service()
    
    # Step 1: Create a session
    print("\n📋 STEP 1: Creating User Session")
    print("-" * 80)
    session_data = session_service.create_session(
        user_id="demo-user-001",
        experience_level="intermediate"
    )
    session_id = session_data['session_id']
    print(f"✅ Session created: {session_id}")
    print(f"   Experience Level: {session_data['experience_level']}")
    print(f"   Status: {session_data['status']}")
    
    # Step 2: Create agent workflow
    print("\n🚀 STEP 2: Starting Agent Creation Workflow")
    print("-" * 80)
    print("Use Case: Customer Support Chatbot")
    print("Description: Build an AI-powered chatbot that can:")
    print("  - Handle customer support inquiries 24/7")
    print("  - Integrate with Salesforce CRM")
    print("  - Support 1000+ concurrent users")
    print("  - Provide responses in under 2 seconds")
    
    agent_data = await workflow_service.create_agent_workflow(
        session_id=session_id,
        user_id="demo-user-001",
        use_case="customer_support_chatbot",
        description="""
        Build an AI-powered customer support chatbot that can handle high-volume 
        inquiries, integrate with our Salesforce CRM system, and provide instant 
        responses. The chatbot should support 1000+ concurrent users with response 
        times under 2 seconds. Budget is approximately $50/month.
        """,
        experience_level="intermediate"
    )
    
    agent_id = agent_data['agent_id']
    print(f"\n✅ Agent workflow created: {agent_id}")
    print(f"   Current Phase: {agent_data['status']}")
    print(f"   Progress: {agent_data['progress_percentage']:.1f}%")
    print(f"   Vector Search: {'Enabled' if agent_data['vector_search_enabled'] else 'Disabled'}")
    
    # Step 3: Submit detailed requirements
    print("\n📝 STEP 3: Submitting Detailed Requirements")
    print("-" * 80)
    print("Consulting with AWS Solutions Architect...")
    
    requirements_result = await workflow_service.submit_requirements(
        agent_id=agent_id,
        user_input="""
        Requirements:
        - Handle 1000+ concurrent users
        - Response time < 2 seconds
        - Integrate with Salesforce CRM via REST API
        - Support natural language understanding
        - 24/7 availability with 99.9% uptime
        - Budget: $50/month
        - Timeline: 2 weeks for MVP
        """,
        context={
            'budget_range': 'medium',
            'timeline': '2_weeks',
            'expected_users': 1000,
            'integrations': ['salesforce_crm']
        }
    )
    
    analysis = requirements_result.get('analysis', {})
    print(f"\n✅ Requirements analyzed")
    print(f"   Confidence Score: {analysis.get('confidence_score', 0):.1%}")
    
    # Show service recommendations
    service_recs = analysis.get('service_recommendations', [])
    if service_recs:
        print(f"\n   📦 Service Recommendations ({len(service_recs)} services):")
        for i, rec in enumerate(service_recs[:5], 1):
            if isinstance(rec, dict):
                service_name = rec.get('service_name', 'Unknown')
                reasoning = rec.get('reasoning', 'No reasoning provided')
                print(f"      {i}. {service_name}")
                print(f"         → {reasoning[:80]}...")
    
    # Show cost analysis
    cost_analysis = analysis.get('cost_analysis', {})
    if cost_analysis:
        print(f"\n   💰 Cost Analysis:")
        estimated_cost = cost_analysis.get('estimated_monthly_cost', 'N/A')
        print(f"      Estimated Monthly Cost: {estimated_cost}")
    
    # Show clarifying questions
    questions = analysis.get('clarifying_questions', [])
    if questions:
        print(f"\n   ❓ Clarifying Questions ({len(questions)}):")
        for i, question in enumerate(questions[:3], 1):
            print(f"      {i}. {question}")
    
    # Step 4: User asks for clarification
    print("\n💬 STEP 4: User Requests Clarification")
    print("-" * 80)
    print("User: 'Can you explain more about the cost breakdown?'")
    
    clarification_result = await workflow_service.process_feedback(
        agent_id=agent_id,
        feedback_type="clarification",
        content="Can you explain more about the cost breakdown and how we can optimize it?",
        rating=4
    )
    
    print(f"\n✅ Clarification processed")
    print(f"   Action: {clarification_result['action']}")
    print(f"   Response: {clarification_result['message']}")
    
    # Step 5: Get current recommendations
    print("\n🎯 STEP 5: Retrieving AI Recommendations")
    print("-" * 80)
    
    recommendations = await workflow_service.get_recommendations(
        agent_id=agent_id,
        recommendation_type="services"
    )
    
    print(f"✅ Recommendations retrieved")
    print(f"   Current Phase: {recommendations['current_phase']}")
    print(f"   Confidence Score: {recommendations['confidence_score']:.1%}")
    print(f"   Total Recommendations: {len(recommendations['recommendations'])}")
    
    # Step 6: User approves and proceeds
    print("\n👍 STEP 6: User Approves Requirements")
    print("-" * 80)
    print("User: 'Looks great! Let's proceed to architecture design.'")
    
    approval_result = await workflow_service.process_feedback(
        agent_id=agent_id,
        feedback_type="approval",
        content="Looks great! The recommendations make sense. Let's proceed.",
        rating=5
    )
    
    print(f"\n✅ Approval processed")
    print(f"   Action: {approval_result['action']}")
    print(f"   Next Phase: {approval_result.get('next_phase', 'N/A')}")
    print(f"   Message: {approval_result['message']}")
    
    # Step 7: Check final status
    print("\n📊 STEP 7: Checking Workflow Status")
    print("-" * 80)
    
    final_status = await workflow_service.get_workflow_status(agent_id)
    
    print(f"✅ Workflow status:")
    print(f"   Agent ID: {final_status['agent_id']}")
    print(f"   Current Phase: {final_status['status']}")
    print(f"   Progress: {final_status['progress_percentage']:.1f}%")
    print(f"   Completed Steps: {len(final_status['completed_steps'])}")
    print(f"   Created: {final_status['created_at']}")
    print(f"   Last Updated: {final_status['updated_at']}")
    
    # Summary
    print("\n" + "=" * 80)
    print("WORKFLOW DEMO COMPLETE")
    print("=" * 80)
    print(f"✅ Session created: {session_id}")
    print(f"✅ Agent workflow initialized: {agent_id}")
    print(f"✅ Requirements analyzed with {analysis.get('confidence_score', 0):.1%} confidence")
    print(f"✅ {len(service_recs)} AWS services recommended")
    print(f"✅ User feedback processed (clarification + approval)")
    print(f"✅ Ready to proceed to architecture phase")
    print("\n🎉 The workflow API is working perfectly!")
    print("\nNext Steps:")
    print("  1. Architecture design with Architecture Advisor")
    print("  2. Implementation with Implementation Guide")
    print("  3. Testing with Testing Validator")
    print("  4. Deployment preparation")
    
    return True


async def main():
    """Run the demo"""
    try:
        success = await demo_complete_workflow()
        return 0 if success else 1
    except Exception as e:
        print(f"\n❌ Demo failed: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    exit_code = asyncio.run(main())
    sys.exit(exit_code)
