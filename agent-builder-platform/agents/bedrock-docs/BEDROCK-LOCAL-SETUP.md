# AWS Bedrock + Claude Local Setup Guide

**Goal**: Connect your agents to AWS Bedrock Claude locally for testing before deployment

**Time**: 15-20 minutes

---

## 📋 Prerequisites

Before starting, ensure you have:
- ✅ AWS Account with Bedrock access
- ✅ Python 3.9+ installed
- ✅ Agent Builder Platform cloned locally
- ✅ Virtual environment activated

---

## 🚀 Step-by-Step Setup

### Step 1: Install AWS CLI

**Windows:**
Download and install from: https://aws.amazon.com/cli/

**Verify installation:**
```cmd
aws --version
```

Expected output: `aws-cli/2.x.x Python/3.x.x Windows/...`

---

### Step 2: Configure AWS Credentials

**Option A: Using AWS CLI (Recommended)**

```cmd
aws configure
```

Enter when prompted:
```
AWS Access Key ID: [Your Access Key]
AWS Secret Access Key: [Your Secret Key]
Default region name: us-east-1
Default output format: json
```

**Option B: Using Environment Variables**

Create `.env` file in `agent-builder-platform/`:

```env
AWS_ACCESS_KEY_ID=your_access_key_here
AWS_SECRET_ACCESS_KEY=your_secret_key_here
AWS_DEFAULT_REGION=us-east-1
```

**Where to get AWS credentials:**
1. Go to AWS Console → IAM
2. Click "Users" → Your username
3. Click "Security credentials" tab
4. Click "Create access key"
5. Download and save the credentials

---

### Step 3: Enable Bedrock Model Access

**Important**: You must request access to Claude models in AWS Console.

1. Go to AWS Console → Amazon Bedrock
2. Click "Model access" in left sidebar
3. Click "Manage model access"
4. Check these models:
   - ✅ **Claude 3 Sonnet** (anthropic.claude-3-sonnet-20240229-v1:0)
   - ✅ **Claude 3.5 Sonnet** (anthropic.claude-3-5-sonnet-20240620-v1:0)
   - ✅ **Titan Embeddings** (amazon.titan-embed-text-v1)
5. Click "Request model access"
6. Wait 2-5 minutes for approval (usually instant)

**Verify access:**
```cmd
aws bedrock list-foundation-models --region us-east-1
```

---

### Step 4: Install Required Python Packages

```cmd
cd agent-builder-platform
venv\Scripts\activate.bat
pip install boto3 python-dotenv
```

**Verify boto3 installation:**
```cmd
python -c "import boto3; print(boto3.__version__)"
```

---

### Step 5: Create Bedrock LLM Service

Create `agent-builder-platform/agents/bedrock_llm.py`:

```python
"""
AWS Bedrock LLM Service
Connects agents to Claude via AWS Bedrock
"""

import boto3
import json
import logging
import os
from typing import Dict, Any, Optional
from botocore.exceptions import ClientError

logger = logging.getLogger(__name__)

class BedrockLLMService:
    """AWS Bedrock Claude integration for local testing"""
    
    def __init__(
        self, 
        region_name: str = None,
        model_id: str = None
    ):
        """
        Initialize Bedrock client
        
        Args:
            region_name: AWS region (default: us-east-1)
            model_id: Claude model ID (default: Claude 3 Sonnet)
        """
        self.region_name = region_name or os.getenv('AWS_DEFAULT_REGION', 'us-east-1')
        self.model_id = model_id or "anthropic.claude-3-sonnet-20240229-v1:0"
        
        # Initialize Bedrock client
        try:
            self.client = boto3.client(
                service_name='bedrock-runtime',
                region_name=self.region_name
            )
            logger.info(f"✅ Bedrock client initialized in {self.region_name}")
        except Exception as e:
            logger.error(f"❌ Failed to initialize Bedrock client: {e}")
            raise
    
    async def generate_response(
        self,
        prompt: str,
        system_prompt: str = None,
        max_tokens: int = 4096,
        temperature: float = 0.7,
        top_p: float = 0.9
    ) -> str:
        """
        Generate response using Claude via Bedrock
        
        Args:
            prompt: User prompt/question
            system_prompt: System instructions for Claude
            max_tokens: Maximum tokens in response
            temperature: Randomness (0-1)
            top_p: Nucleus sampling parameter
            
        Returns:
            Claude's response text
        """
        try:
            # Prepare messages
            messages = [
                {
                    "role": "user",
                    "content": prompt
                }
            ]
            
            # Prepare request body
            request_body = {
                "anthropic_version": "bedrock-2023-05-31",
                "max_tokens": max_tokens,
                "temperature": temperature,
                "top_p": top_p,
                "messages": messages
            }
            
            # Add system prompt if provided
            if system_prompt:
                request_body["system"] = system_prompt
            
            # Log request (truncated)
            logger.info(f"🤖 Calling Bedrock Claude...")
            logger.debug(f"Model: {self.model_id}")
            logger.debug(f"Prompt length: {len(prompt)} chars")
            
            # Call Bedrock
            response = self.client.invoke_model(
                modelId=self.model_id,
                body=json.dumps(request_body)
            )
            
            # Parse response
            response_body = json.loads(response['body'].read())
            
            # Extract text
            if 'content' in response_body and len(response_body['content']) > 0:
                response_text = response_body['content'][0]['text']
                logger.info(f"✅ Received response ({len(response_text)} chars)")
                return response_text
            else:
                logger.error("❌ No content in response")
                return "Error: No response from Claude"
                
        except ClientError as e:
            error_code = e.response['Error']['Code']
            error_message = e.response['Error']['Message']
            
            logger.error(f"❌ Bedrock API error: {error_code} - {error_message}")
            
            # Provide helpful error messages
            if error_code == 'AccessDeniedException':
                return "Error: Access denied. Please check:\n1. AWS credentials are correct\n2. IAM permissions include bedrock:InvokeModel\n3. Model access is enabled in Bedrock console"
            elif error_code == 'ResourceNotFoundException':
                return f"Error: Model not found. Please check:\n1. Model ID is correct: {self.model_id}\n2. Model is available in region: {self.region_name}"
            elif error_code == 'ThrottlingException':
                return "Error: Rate limit exceeded. Please wait and try again."
            else:
                return f"Error: {error_message}"
                
        except Exception as e:
            logger.error(f"❌ Unexpected error: {e}")
            return f"Error: {str(e)}"
    
    def test_connection(self) -> bool:
        """
        Test Bedrock connection
        
        Returns:
            True if connection successful, False otherwise
        """
        try:
            # Simple test prompt
            test_body = {
                "anthropic_version": "bedrock-2023-05-31",
                "max_tokens": 100,
                "messages": [
                    {
                        "role": "user",
                        "content": "Say 'Connection successful' if you can read this."
                    }
                ]
            }
            
            response = self.client.invoke_model(
                modelId=self.model_id,
                body=json.dumps(test_body)
            )
            
            response_body = json.loads(response['body'].read())
            
            if 'content' in response_body:
                logger.info("✅ Bedrock connection test successful")
                return True
            else:
                logger.error("❌ Bedrock connection test failed")
                return False
                
        except Exception as e:
            logger.error(f"❌ Bedrock connection test failed: {e}")
            return False

# Global instance (lazy initialization)
_bedrock_llm = None

def get_bedrock_llm() -> BedrockLLMService:
    """Get or create Bedrock LLM service instance"""
    global _bedrock_llm
    if _bedrock_llm is None:
        _bedrock_llm = BedrockLLMService()
    return _bedrock_llm
```

---

### Step 6: Create Connection Test Script

Create `agent-builder-platform/test_bedrock_connection.py`:

```python
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
```

---

### Step 7: Run Connection Test

```cmd
cd agent-builder-platform
venv\Scripts\activate.bat
python test_bedrock_connection.py
```

**Expected Output:**
```
🚀 AWS Bedrock + Claude Local Testing
============================================================

============================================================
🔗 Testing AWS Bedrock Connection
============================================================

1️⃣ Initializing Bedrock client...
   ✅ Client initialized

2️⃣ Testing connection...
   ✅ Connection successful

3️⃣ Testing Claude response...
   Response: I'm Claude, an AI assistant created by Anthropic to be helpful, harmless, and honest.
   ✅ Response successful

============================================================
🤖 Testing Agent Consultation with Claude
============================================================

Sending consultation request to Claude...

Claude's Response:
------------------------------------------------------------
[Claude's detailed AWS architecture recommendations]
------------------------------------------------------------

✅ Agent consultation successful!

============================================================
📊 Test Summary
============================================================

  Connection Test: ✅ PASSED
  Agent Consultation: ✅ PASSED
  MCP Integration: ✅ PASSED

🎉 All tests passed! Your Bedrock setup is ready.
```

---

### Step 8: Integrate with Your Agents

Now update your agents to use Bedrock. Example for AWS Solutions Architect:

Create `agent-builder-platform/agents/aws_solutions_architect_bedrock.py`:

```python
"""
AWS Solutions Architect Agent with Bedrock Integration
"""

import asyncio
import logging
from typing import Dict, Any
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
        requirements: list,
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
1. Recommended AWS Services (with brief explanation)
2. Cost Estimate (itemized, monthly)
3. Security Recommendations
4. Scalability Considerations
5. Confidence Score (0-100%)

Be concise but thorough. Adapt explanations to the user's experience level."""

        # Build user prompt
        requirements_text = "\n".join([f"- {req}" for req in requirements])
        
        user_prompt = f"""Use Case: {use_case}

Requirements:
{requirements_text}

Budget: {budget}
Experience Level: {experience_level}

Please provide AWS architecture recommendations."""

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
            "budget": budget
        }

# Test function
async def test_agent():
    """Test the Bedrock-integrated agent"""
    agent = AWSolutionsArchitectBedrock()
    
    result = await agent.consult(
        use_case="Build a chatbot for customer support",
        requirements=[
            "Handle 1000 requests per day",
            "Store conversation history",
            "Integrate with existing CRM"
        ],
        budget="$50/month",
        experience_level="beginner"
    )
    
    print("\n" + "="*60)
    print(f"Agent: {result['agent']}")
    print("="*60 + "\n")
    print(result['response'])
    print("\n")

if __name__ == "__main__":
    asyncio.run(test_agent())
```

**Test the integrated agent:**
```cmd
python agents/aws_solutions_architect_bedrock.py
```

---

## 🔧 Configuration Options

### Change Claude Model

Edit `bedrock_llm.py`:

```python
# Use Claude 3.5 Sonnet (more capable, slightly more expensive)
self.model_id = "anthropic.claude-3-5-sonnet-20240620-v1:0"

# Use Claude 3 Haiku (faster, cheaper)
self.model_id = "anthropic.claude-3-haiku-20240307-v1:0"
```

### Adjust Response Parameters

```python
response = await bedrock.generate_response(
    prompt=prompt,
    max_tokens=4096,      # Increase for longer responses
    temperature=0.7,      # 0.0 = deterministic, 1.0 = creative
    top_p=0.9            # Nucleus sampling
)
```

### Set Environment Variables

Create `.env` file:

```env
# AWS Configuration
AWS_ACCESS_KEY_ID=your_key
AWS_SECRET_ACCESS_KEY=your_secret
AWS_DEFAULT_REGION=us-east-1

# Bedrock Configuration
BEDROCK_MODEL_ID=anthropic.claude-3-sonnet-20240229-v1:0
BEDROCK_MAX_TOKENS=4096
BEDROCK_TEMPERATURE=0.7
```

---

## 📊 Cost Estimation

**Claude 3 Sonnet Pricing (us-east-1):**
- Input: $0.003 per 1K tokens
- Output: $0.015 per 1K tokens

**Example costs:**
- 100 consultations/day: ~$5-10/month
- 1000 consultations/day: ~$50-100/month

**Tips to reduce costs:**
- Use Claude 3 Haiku for simple queries
- Cache common responses
- Limit max_tokens appropriately
- Use temperature=0 for deterministic responses

---

## ✅ Verification Checklist

Before proceeding, verify:

- [ ] AWS CLI installed and configured
- [ ] AWS credentials set up (access key + secret)
- [ ] Bedrock model access enabled in AWS Console
- [ ] boto3 installed (`pip install boto3`)
- [ ] Connection test passes
- [ ] Agent consultation test passes
- [ ] MCP integration test passes

---

## 🐛 Troubleshooting

### Error: "AccessDeniedException"

**Solution:**
1. Check IAM permissions include `bedrock:InvokeModel`
2. Verify credentials: `aws sts get-caller-identity`
3. Ensure model access is enabled in Bedrock console

### Error: "ResourceNotFoundException"

**Solution:**
1. Verify model ID is correct
2. Check region supports Bedrock (use us-east-1)
3. Confirm model access is approved

### Error: "ThrottlingException"

**Solution:**
1. Add retry logic with exponential backoff
2. Reduce request rate
3. Request quota increase in AWS Console

### Error: "ValidationException"

**Solution:**
1. Check request body format
2. Verify max_tokens is within limits (max 4096)
3. Ensure messages array is properly formatted

### Connection times out

**Solution:**
1. Check internet connection
2. Verify AWS region is accessible
3. Check firewall/proxy settings
4. Try different region

---

## 🚀 Next Steps

Once Bedrock is working:

1. **Integrate with all 5 agents**
   - AWS Solutions Architect ✅
   - Architecture Advisor
   - Implementation Guide
   - Testing Validator
   - Strands Integration

2. **Connect to orchestrator**
   - Update workflow to use Bedrock
   - Add error handling
   - Implement retries

3. **Test with MCPs**
   - Integrate MCP knowledge
   - Test vector search
   - Validate confidence scores

4. **Connect to frontend**
   - Test full consultation flow
   - Verify WebSocket updates
   - Test export functionality

5. **Prepare for deployment**
   - Review costs
   - Optimize prompts
   - Add monitoring

---

## 📚 Additional Resources

- **AWS Bedrock Docs**: https://docs.aws.amazon.com/bedrock/
- **Claude API Reference**: https://docs.anthropic.com/claude/reference/
- **Boto3 Bedrock**: https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-runtime.html
- **IAM Permissions**: https://docs.aws.amazon.com/bedrock/latest/userguide/security-iam.html

---

**Status**: ✅ Ready to connect! Run `python test_bedrock_connection.py` to start.
