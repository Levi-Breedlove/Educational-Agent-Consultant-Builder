#!/usr/bin/env python3
"""
Simple Demo for Agent Creation Workflow API
Demonstrates workflow service without external dependencies
"""

import asyncio
import sys
import os

sys.path.insert(0, os.path.dirname(__file__))

from workflow_service import get_workflow_service


async def simple_demo():
    """Simple workflow demonstration"""
    print("=" * 80)
    print("AGENT CREATION WORKFLOW - SIMPLE DEMO")
    print("=" * 80)
    
    workflow_service = get_workflow_service()
    
    print("\n✅ Workflow service initialized")
    print("   - Manager Agent orchestrator ready")
    print("   - AWS Solutions Architect agent ready")
    print("   - Vector search capabilities available")
    
    # Create workflow
    print("\n🚀 Creating agent workflow...")
    agent_data = await workflow_service.create_agent_workflow(
        session_id="demo-session",
        user_id="demo-user",
        use_case="customer_support_chatbot",
        description="Build an AI chatbot for customer support with CRM integration",
        experience_level="intermediate"
    )
    
    agent_id = agent_data['agent_id']
    print(f"✅ Agent created: {agent_id}")
    print(f"   Phase: {agent_data['status']}")
    print(f"   Progress: {agent_data['progress_percentage']:.1f}%")
    
    # Submit requirements
    print("\n📝 Submitting requirements...")
    result = await workflow_service.submit_requirements(
        agent_id=agent_id,
        user_input="Need to handle 1000+ users with <2s response time, integrate with Salesforce",
        context={'budget_range': 'medium'}
    )
    
    analysis = result.get('analysis', {})
    print(f"✅ Requirements analyzed")
    print(f"   Confidence: {analysis.get('confidence_score', 0):.1%}")
    print(f"   Services: {len(analysis.get('service_recommendations', []))}")
    
    # Get status
    print("\n📊 Checking status...")
    status = await workflow_service.get_workflow_status(agent_id)
    print(f"✅ Status: {status['status']}")
    print(f"   Progress: {status['progress_percentage']:.1f}%")
    
    print("\n🎉 Demo complete! Workflow API is operational.")
    return True


if __name__ == "__main__":
    try:
        asyncio.run(simple_demo())
        sys.exit(0)
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)
