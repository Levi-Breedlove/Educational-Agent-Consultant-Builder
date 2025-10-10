"""
AWS Solutions Architect Agent with Bedrock Integration
Example of how to integrate Bedrock Claude into your agents
"""

import asyncio
import logging
from typing import Dict, Any, List
from agents.bedrock_llm import get_bedrock_llm

logger = logging.getLogger(__name__)

class AWSolutionsArchitectBedrock:
    """AWS Solutions Architect using Bedrock Claude"""
    
    def __init__(self):
        self.llm = get_bedrock_llm()
        self.agent_name = "AWS Solutions Architect"
        
    async def consult(
        self,
        use_case: str,
        requirements: List[str],
        budget: str,
        experience_level: str = "beginner"
    ) -> Dict[str, Any]:
        """
        Provide AWS architecture consultation
        
        Args:
            use_case: User's use case description
            requirements: List of requirements
            budget: Monthly budget
            experience_level: User's experience level
            
        Returns:
            Consultation response with recommendations
        """
        
        # Build system prompt
        system_prompt = f"""You are an expert AWS Solutions Architect providing consultation to a {experience_level} user.

Your role:
- Recommend appropriate AWS services
- Provide accurate cost estimates
- Explain trade-offs clearly
- Ensure security best practices
- Stay within budget constraints

Response format:
1. **Recommended AWS Services** (with brief explanation for each)
2. **Cost Estimate** (itemized, monthly)
3. **Security Recommendations** (specific to the use case)
4. **Scalability Considerations** (how it will scale)
5. **Confidence Score** (0-100% based on requirements clarity)

Be concise but thorough. Adapt explanations to the user's experience level.
For beginners, explain AWS concepts. For experts, focus on advanced optimizations."""

        # Build user prompt
        requirements_text = "\n".join([f"- {req}" for req in requirements])
        
        user_prompt = f"""Use Case: {use_case}

Requirements:
{requirements_text}

Budget: {budget}
Experience Level: {experience_level}

Please provide AWS architecture recommendations that meet these requirements and stay within budget."""

        # Get response from Claude
        logger.info(f"🤖 {self.agent_name} consulting...")
        
        response = await self.llm.generate_response(
            prompt=user_prompt,
            system_prompt=system_prompt,
            max_tokens=3000,
            temperature=0.7
        )
        
        return {
            "agent": self.agent_name,
            "response": response,
            "use_case": use_case,
            "budget": budget,
            "experience_level": experience_level
        }
    
    async def follow_up(
        self,
        previous_response: str,
        question: str
    ) -> str:
        """
        Handle follow-up questions
        
        Args:
            previous_response: Previous consultation response
            question: Follow-up question
            
        Returns:
            Follow-up response
        """
        system_prompt = """You are an AWS Solutions Architect in a follow-up conversation.
Reference the previous recommendations and provide additional clarification or details."""
        
        user_prompt = f"""Previous Recommendation:
{previous_response[:500]}...

Follow-up Question: {question}

Please provide a detailed answer."""
        
        response = await self.llm.generate_response(
            prompt=user_prompt,
            system_prompt=system_prompt,
            max_tokens=2000,
            temperature=0.7
        )
        
        return response

# Test function
async def test_agent():
    """Test the Bedrock-integrated agent"""
    print("\n" + "="*60)
    print("🤖 Testing AWS Solutions Architect with Bedrock")
    print("="*60 + "\n")
    
    agent = AWSolutionsArchitectBedrock()
    
    # Test consultation
    print("📋 Consultation Request:")
    print("  Use Case: Build a chatbot for customer support")
    print("  Budget: $50/month")
    print("  Experience: Beginner\n")
    
    result = await agent.consult(
        use_case="Build a chatbot for customer support",
        requirements=[
            "Handle 1000 requests per day",
            "Store conversation history",
            "Integrate with existing CRM",
            "Support multiple languages"
        ],
        budget="$50/month",
        experience_level="beginner"
    )
    
    print("="*60)
    print(f"Agent: {result['agent']}")
    print("="*60 + "\n")
    print(result['response'])
    print("\n")
    
    # Test follow-up
    print("="*60)
    print("💬 Follow-up Question")
    print("="*60 + "\n")
    
    follow_up_response = await agent.follow_up(
        previous_response=result['response'],
        question="How would I implement the CRM integration specifically?"
    )
    
    print(follow_up_response)
    print("\n")

async def test_multiple_scenarios():
    """Test multiple consultation scenarios"""
    print("\n" + "="*60)
    print("🧪 Testing Multiple Scenarios")
    print("="*60 + "\n")
    
    agent = AWSolutionsArchitectBedrock()
    
    scenarios = [
        {
            "use_case": "Real-time data processing pipeline",
            "requirements": [
                "Process 10,000 events per second",
                "Store results in database",
                "Generate real-time analytics"
            ],
            "budget": "$200/month",
            "experience_level": "advanced"
        },
        {
            "use_case": "Simple REST API for mobile app",
            "requirements": [
                "Handle 100 requests per day",
                "Store user data",
                "Send push notifications"
            ],
            "budget": "$20/month",
            "experience_level": "beginner"
        }
    ]
    
    for i, scenario in enumerate(scenarios, 1):
        print(f"\n{'='*60}")
        print(f"Scenario {i}: {scenario['use_case']}")
        print('='*60 + "\n")
        
        result = await agent.consult(**scenario)
        
        print(result['response'])
        print("\n")

async def main():
    """Run all tests"""
    print("\n🚀 AWS Solutions Architect Bedrock Integration Test\n")
    
    # Test basic consultation
    await test_agent()
    
    # Test multiple scenarios
    # await test_multiple_scenarios()
    
    print("✅ All tests completed!\n")

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
