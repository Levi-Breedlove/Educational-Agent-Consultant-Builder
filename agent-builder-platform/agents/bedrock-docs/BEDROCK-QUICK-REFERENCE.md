# AWS Bedrock Quick Reference

**Quick commands for testing Bedrock locally**

---

## 🚀 Quick Start (5 Minutes)

```cmd
# 1. Configure AWS
aws configure

# 2. Test connection
cd agent-builder-platform
venv\Scripts\activate.bat
python test_bedrock_connection.py
```

---

## 📋 AWS Configuration

### Set Credentials
```cmd
aws configure
```

### Verify Credentials
```cmd
aws sts get-caller-identity
```

### Check Bedrock Access
```cmd
aws bedrock list-foundation-models --region us-east-1
```

---

## 🔑 Required IAM Permissions

Add to your IAM user/role:

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "bedrock:InvokeModel",
        "bedrock:InvokeModelWithResponseStream"
      ],
      "Resource": "*"
    }
  ]
}
```

---

## 🤖 Claude Models

| Model | ID | Use Case | Cost |
|-------|-----|----------|------|
| **Claude 3.5 Sonnet** | `anthropic.claude-3-5-sonnet-20240620-v1:0` | Most capable | $$$ |
| **Claude 3 Sonnet** | `anthropic.claude-3-sonnet-20240229-v1:0` | Balanced | $$ |
| **Claude 3 Haiku** | `anthropic.claude-3-haiku-20240307-v1:0` | Fast & cheap | $ |

---

## 💻 Code Examples

### Basic Usage

```python
from agents.bedrock_llm import get_bedrock_llm

# Get LLM service
bedrock = get_bedrock_llm()

# Generate response
response = await bedrock.generate_response(
    prompt="Your question here",
    system_prompt="You are an expert...",
    max_tokens=2000,
    temperature=0.7
)

print(response)
```

### With Agent

```python
from agents.bedrock_llm import get_bedrock_llm

class MyAgent:
    def __init__(self):
        self.llm = get_bedrock_llm()
    
    async def consult(self, user_input):
        response = await self.llm.generate_response(
            prompt=user_input,
            system_prompt="You are an AWS expert...",
            max_tokens=3000
        )
        return response
```

---

## 🔧 Configuration

### Environment Variables

Create `.env`:

```env
AWS_ACCESS_KEY_ID=your_key
AWS_SECRET_ACCESS_KEY=your_secret
AWS_DEFAULT_REGION=us-east-1
BEDROCK_MODEL_ID=anthropic.claude-3-sonnet-20240229-v1:0
```

### Change Model

```python
bedrock = BedrockLLMService(
    model_id="anthropic.claude-3-5-sonnet-20240620-v1:0"
)
```

### Adjust Parameters

```python
response = await bedrock.generate_response(
    prompt=prompt,
    max_tokens=4096,      # Max response length
    temperature=0.7,      # 0=deterministic, 1=creative
    top_p=0.9            # Nucleus sampling
)
```

---

## 🐛 Common Errors

### AccessDeniedException
**Fix**: Enable model access in Bedrock console

### ResourceNotFoundException
**Fix**: Check model ID and region

### ThrottlingException
**Fix**: Add retry logic or reduce request rate

### ValidationException
**Fix**: Check request format and token limits

---

## 💰 Cost Tracking

### Check Usage
```cmd
aws ce get-cost-and-usage \
  --time-period Start=2024-01-01,End=2024-01-31 \
  --granularity MONTHLY \
  --metrics BlendedCost \
  --filter file://bedrock-filter.json
```

### Estimate Costs

**Claude 3 Sonnet (us-east-1):**
- Input: $0.003 / 1K tokens
- Output: $0.015 / 1K tokens

**Example:**
- 1000 consultations/day
- ~500 tokens input, ~1500 tokens output each
- Cost: ~$50-100/month

---

## ✅ Testing Checklist

- [ ] AWS CLI installed
- [ ] Credentials configured
- [ ] Bedrock access enabled
- [ ] Connection test passes
- [ ] Agent test passes
- [ ] MCP test passes

---

## 📚 Resources

- **Setup Guide**: `BEDROCK-LOCAL-SETUP.md`
- **AWS Bedrock**: https://aws.amazon.com/bedrock/
- **Claude Docs**: https://docs.anthropic.com/claude/
- **Boto3 Docs**: https://boto3.amazonaws.com/

---

## 🆘 Get Help

1. Check `BEDROCK-LOCAL-SETUP.md` for detailed instructions
2. Run `python test_bedrock_connection.py` for diagnostics
3. Review AWS CloudWatch logs
4. Check IAM permissions

---

**Quick Test**: `python test_bedrock_connection.py`
