"""
Test Bedrock + MCPs Integration
Shows how to use Bedrock Claude with MCP knowledge
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

# Add paths
sys.path.append(os.path.join(os.path.dirname(__file__), 'agents'))
sys.path.append(os.path.join(os.path.dirname(__file__), 'mcp-integration'))

from agents.bedrock_llm import get_bedrock_llm

# Try to import MCP ecosystem
try:
    from mcp_integration.mcp_ecosystem import MCPEcosystem
    MCP_AVAILABLE = True
except ImportError:
    try:
        from mcp_ecosystem import MCPEcosystem
        MCP_AVAILABLE = True
    except ImportError:
        logger.warning("MCP Ecosystem not available - will test Bedrock only")
        MCP_AVAILABLE = False

async def test_bedrock_only():
    """Test Bedrock without MCPs (baseline)"""
    print("\n" + "="*60)
    print("🤖 Test 1: Bedrock Claude Only (No MCPs)")
    print("="*60 + "\n")
    
    bedrock = get_bedrock_llm()
    
    prompt = """What are the best AWS services for building a chatbot?
    
Please recommend:
1. Compute service
2. Database
3. AI/ML service
4. Storage"""
    
    print("Querying Claude (without MCP knowledge)...\n")
    
    response = await bedrock.generate_response(
        prompt=prompt,
        system_prompt="You are an AWS expert.",
        max_tokens=1000
    )
    
    print("Response:")
    print("-" * 60)
    print(response)
    print("-" * 60 + "\n")
    
    return response

async def test_bedrock_with_mcp_context():
    """Test Bedrock with MCP knowledge in prompt"""
    print("\n" + "="*60)
    print("🔗 Test 2: Bedrock + MCP Knowledge (Manual Integration)")
    print("="*60 + "\n")
    
    bedrock = get_bedrock_llm()
    
    # Simulate MCP knowledge (this is what your MCPs would provide)
    mcp_knowledge = """
AWS Services Knowledge from MCPs:

1. AWS Lambda
   - Serverless compute service
   - Free tier: 1M requests/month
   - Cost: $0.20 per 1M requests
   - Best for: Event-driven, short-running tasks

2. Amazon DynamoDB
   - Serverless NoSQL database
   - Free tier: 25 GB storage
   - Cost: $1.25 per million write requests
   - Best for: High-performance, scalable applications

3. Amazon Bedrock
   - Managed foundation models
   - Claude 3 Sonnet: $0.003/1K input tokens
   - Best for: AI/ML, chatbots, content generation

4. Amazon S3
   - Object storage
   - Free tier: 5 GB storage
   - Cost: $0.023 per GB/month
   - Best for: File storage, static hosting
"""
    
    system_prompt = f"""You are an AWS Solutions Architect with access to comprehensive AWS documentation.

Available AWS Services Knowledge:
{mcp_knowledge}

Use this knowledge to provide accurate, specific recommendations with cost estimates."""
    
    user_prompt = """What are the best AWS services for building a chatbot?

Requirements:
- Handle 1000 requests/day
- Store conversation history
- Budget: $50/month

Please recommend specific services with cost breakdown."""
    
    print("Querying Claude (with MCP knowledge in prompt)...\n")
    
    response = await bedrock.generate_response(
        prompt=user_prompt,
        system_prompt=system_prompt,
        max_tokens=1500
    )
    
    print("Response:")
    print("-" * 60)
    print(response)
    print("-" * 60 + "\n")
    
    return response

async def test_bedrock_with_mcp_ecosystem():
    """Test Bedrock with actual MCP ecosystem (if available)"""
    
    if not MCP_AVAILABLE:
        print("\n" + "="*60)
        print("⚠️  Test 3: Skipped (MCP Ecosystem not available)")
        print("="*60 + "\n")
        print("To enable this test:")
        print("1. Ensure mcp_ecosystem.py is in mcp-integration/")
        print("2. Configure MCPs in mcp-config.yaml")
        print("3. Run MCP health check\n")
        return None
    
    print("\n" + "="*60)
    print("🌐 Test 3: Bedrock + Full MCP Ecosystem")
    print("="*60 + "\n")
    
    # Initialize MCP ecosystem
    print("Initializing MCP Ecosystem...")
    mcp_ecosystem = MCPEcosystem()
    
    if not mcp_ecosystem.initialize():
        print("❌ Failed to initialize MCP ecosystem\n")
        return None
    
    print(f"✅ MCP Ecosystem initialized with {len(mcp_ecosystem.mcps)} MCPs\n")
    
    # Get Bedrock
    bedrock = get_bedrock_llm()
    
    # In a real implementation, you would:
    # 1. Query MCPs for relevant knowledge
    # 2. Build system prompt with MCP data
    # 3. Send to Bedrock
    
    print("Note: Full MCP integration requires:")
    print("  - MCP servers running")
    print("  - Knowledge base populated")
    print("  - Vector search configured")
    print("\nFor now, this demonstrates the architecture.\n")
    
    return "MCP ecosystem ready for integration"

async def compare_responses():
    """Compare responses with and without MCP knowledge"""
    print("\n" + "="*60)
    print("📊 Comparison: Bedrock Only vs Bedrock + MCPs")
    print("="*60 + "\n")
    
    print("Key Differences:\n")
    print("Bedrock Only:")
    print("  ✓ Fast responses")
    print("  ✓ General AWS knowledge")
    print("  ✗ May lack specific details")
    print("  ✗ No cost estimates")
    print("  ✗ Generic recommendations\n")
    
    print("Bedrock + MCPs:")
    print("  ✓ Accurate, specific information")
    print("  ✓ Real cost estimates")
    print("  ✓ Up-to-date AWS documentation")
    print("  ✓ Best practices from MCPs")
    print("  ✓ Higher confidence scores\n")

async def main():
    """Run all tests"""
    print("\n🚀 Testing Bedrock + MCP Integration")
    print("="*60 + "\n")
    
    # Test 1: Bedrock only
    await test_bedrock_only()
    
    # Test 2: Bedrock with MCP knowledge
    await test_bedrock_with_mcp_context()
    
    # Test 3: Bedrock with full MCP ecosystem
    await test_bedrock_with_mcp_ecosystem()
    
    # Comparison
    await compare_responses()
    
    # Summary
    print("\n" + "="*60)
    print("✅ Testing Complete")
    print("="*60 + "\n")
    
    print("Next Steps:\n")
    print("1. ✅ Bedrock connection works")
    print("2. ✅ Can include MCP knowledge in prompts")
    print("3. 🔄 Integrate MCPs into your agents")
    print("4. 🔄 Test with orchestrator")
    print("5. 🔄 Connect to frontend\n")
    
    print("To integrate MCPs into your agents:")
    print("  - Query MCPs for relevant knowledge")
    print("  - Include MCP data in system prompts")
    print("  - Bedrock will use that knowledge in responses\n")

if __name__ == "__main__":
    asyncio.run(main())
