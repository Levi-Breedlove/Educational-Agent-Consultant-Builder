"""
Test AWS Bedrock Connection
Verifies credentials, permissions, and model access
"""

import asyncio
import sys
import os
import logging

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Add agents to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'agents'))

from agents.bedrock_llm import BedrockLLMService

async def test_connection():
    """Test basic Bedrock connection"""
    print("\n" + "="*60)
    print("🔗 Testing AWS Bedrock Connection")
    print("="*60 + "\n")
    
    try:
        # Initialize service
        print("1️⃣ Initializing Bedrock client...")
        bedrock = BedrockLLMService()
        print("   ✅ Client initialized\n")
        
        # Test connection
        print("2️⃣ Testing connection...")
        if bedrock.test_connection():
            print("   ✅ Connection successful\n")
        else:
            print("   ❌ Connection failed\n")
            return False
        
        # Test simple prompt
        print("3️⃣ Testing Claude response...")
        response = await bedrock.generate_response(
            prompt="Hello! Please introduce yourself in one sentence.",
            max_tokens=100
        )
        print(f"   Response: {response}\n")
        
        if "Error:" in response:
            print("   ❌ Response contains error\n")
            return False
        else:
            print("   ✅ Response successful\n")
        
        return True
        
    except Exception as e:
        print(f"   ❌ Error: {e}\n")
        return False

async def test_agent_consultation():
    """Test agent consultation with Claude"""
    print("\n" + "="*60)
    print("🤖 Testing Agent Consultation with Claude")
    print("="*60 + "\n")
    
    try:
        bedrock = BedrockLLMService()
        
        # Simulate AWS Solutions Architect consultation
        system_prompt = """You are an expert AWS Solutions Architect. 
Provide clear, concise recommendations with cost estimates.
Always include a confidence score (0-100%) at the end."""
        
        user_prompt = """I need to build a chatbot for customer support.

Requirements:
- Handle 1000 requests per day
- Store conversation history
- Integrate with existing CRM
- Budget: $50/month

Please recommend AWS services and provide cost estimates."""
        
        print("Sending consultation request to Claude...\n")
        
        response = await bedrock.generate_response(
            prompt=user_prompt,
            system_prompt=system_prompt,
            max_tokens=2000,
            temperature=0.7
        )
        
        print("Claude's Response:")
        print("-" * 60)
        print(response)
        print("-" * 60 + "\n")
        
        if "Error:" not in response:
            print("✅ Agent consultation successful!\n")
            return True
        else:
            print("❌ Agent consultation failed\n")
            return False
            
    except Exception as e:
        print(f"❌ Error: {e}\n")
        return False

async def test_mcp_integration():
    """Test MCP knowledge integration"""
    print("\n" + "="*60)
    print("📚 Testing MCP Knowledge Integration")
    print("="*60 + "\n")
    
    try:
        bedrock = BedrockLLMService()
        
        # Simulate MCP-enhanced consultation
        system_prompt = """You are an AWS expert with access to comprehensive AWS documentation.
Provide detailed, accurate information based on AWS best practices."""
        
        user_prompt = """What are the best practices for securing AWS Lambda functions?
Include specific recommendations for:
1. IAM roles and permissions
2. VPC configuration
3. Environment variables
4. Encryption"""
        
        print("Querying Claude with MCP context...\n")
        
        response = await bedrock.generate_response(
            prompt=user_prompt,
            system_prompt=system_prompt,
            max_tokens=2000
        )
        
        print("Claude's Response:")
        print("-" * 60)
        print(response)
        print("-" * 60 + "\n")
        
        if "Error:" not in response:
            print("✅ MCP integration test successful!\n")
            return True
        else:
            print("❌ MCP integration test failed\n")
            return False
            
    except Exception as e:
        print(f"❌ Error: {e}\n")
        return False

async def main():
    """Run all tests"""
    print("\n🚀 AWS Bedrock + Claude Local Testing")
    print("="*60 + "\n")
    
    results = []
    
    # Test 1: Connection
    result1 = await test_connection()
    results.append(("Connection Test", result1))
    
    if not result1:
        print("\n❌ Connection test failed. Please check:")
        print("   1. AWS credentials are configured (aws configure)")
        print("   2. Bedrock model access is enabled in AWS Console")
        print("   3. IAM permissions include bedrock:InvokeModel")
        print("   4. Region is set to us-east-1 (or region with Bedrock)")
        return
    
    # Test 2: Agent Consultation
    result2 = await test_agent_consultation()
    results.append(("Agent Consultation", result2))
    
    # Test 3: MCP Integration
    result3 = await test_mcp_integration()
    results.append(("MCP Integration", result3))
    
    # Summary
    print("\n" + "="*60)
    print("📊 Test Summary")
    print("="*60 + "\n")
    
    for test_name, result in results:
        status = "✅ PASSED" if result else "❌ FAILED"
        print(f"  {test_name}: {status}")
    
    all_passed = all(result for _, result in results)
    
    if all_passed:
        print("\n🎉 All tests passed! Your Bedrock setup is ready.")
        print("\n💡 Next Steps:")
        print("   1. Integrate Bedrock into your agents")
        print("   2. Test with the full orchestrator")
        print("   3. Connect to the frontend UI")
        print("   4. Test end-to-end consultation flow\n")
    else:
        print("\n⚠️  Some tests failed. Please review errors above.\n")

if __name__ == "__main__":
    asyncio.run(main())
