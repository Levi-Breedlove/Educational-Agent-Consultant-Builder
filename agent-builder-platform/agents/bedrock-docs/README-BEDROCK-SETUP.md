# 🚀 Get Started with Bedrock + Claude in 15 Minutes

**Complete guide to test your agents with AWS Bedrock Claude locally**

---

## 📚 Documentation Overview

| Document | Purpose | Time |
|----------|---------|------|
| **This File** | Quick overview | 2 min |
| `BEDROCK-LOCAL-SETUP.md` | Complete setup guide | 15 min |
| `BEDROCK-QUICK-REFERENCE.md` | Quick commands | 1 min |
| `test_bedrock_connection.py` | Connection test | 5 min |

---

## ⚡ Quick Start (3 Steps)

### 1. Configure AWS (5 minutes)

```cmd
# Install AWS CLI (if not installed)
# Download from: https://aws.amazon.com/cli/

# Configure credentials
aws configure
```

Enter:
- AWS Access Key ID
- AWS Secret Access Key  
- Region: `us-east-1`
- Output: `json`

### 2. Enable Bedrock Access (5 minutes)

1. Go to AWS Console → Amazon Bedrock
2. Click "Model access" → "Manage model access"
3. Check "Claude 3 Sonnet"
4. Click "Request model access"
5. Wait 2-5 minutes (usually instant)

### 3. Test Connection (5 minutes)

```cmd
cd agent-builder-platform
venv\Scripts\activate.bat
python test_bedrock_connection.py
```

**Expected Output:**
```
🚀 AWS Bedrock + Claude Local Testing
============================================================

🔗 Testing AWS Bedrock Connection
✅ Connection successful

🤖 Testing Agent Consultation with Claude
✅ Agent consultation successful!

📚 Testing MCP Knowledge Integration
✅ MCP integration test successful!

🎉 All tests passed! Your Bedrock setup is ready.
```

---

## 🎯 What You Get

After setup, you can:

✅ **Test agents with real Claude** - No mock responses  
✅ **Use your existing MCPs** - Full knowledge integration  
✅ **Test locally before deployment** - No AWS infrastructure needed  
✅ **Iterate quickly** - Instant feedback loop  
✅ **Control costs** - Pay only for what you test  

---

## 📁 Files Created

```
agent-builder-platform/
├── agents/
│   ├── bedrock_llm.py                      # Bedrock LLM service
│   ├── aws_solutions_architect_bedrock.py  # Example agent
│   └── mock_llm.py                         # Mock for testing
├── test_bedrock_connection.py              # Connection test
├── BEDROCK-LOCAL-SETUP.md                  # Complete guide
├── BEDROCK-QUICK-REFERENCE.md              # Quick commands
└── README-BEDROCK-SETUP.md                 # This file
```

---

## 🧪 Test Your First Agent

```cmd
# Test example agent
python agents/aws_solutions_architect_bedrock.py
```

This will:
1. Connect to Bedrock
2. Send a consultation request
3. Get Claude's response
4. Display recommendations

---

## 💡 Next Steps

### Option 1: Integrate with Existing Agents

Update your agents to use Bedrock:

```python
from agents.bedrock_llm import get_bedrock_llm

class MyAgent:
    def __init__(self):
        self.llm = get_bedrock_llm()
    
    async def consult(self, user_input):
        response = await self.llm.generate_response(
            prompt=user_input,
            system_prompt="You are an expert...",
            max_tokens=3000
        )
        return response
```

### Option 2: Test with Orchestrator

Connect Bedrock to your orchestrator for full workflow testing.

### Option 3: Connect to Frontend

Test the complete consultation flow through the UI.

---

## 💰 Cost Estimate

**Testing costs (Claude 3 Sonnet):**
- 10 tests: ~$0.10
- 100 tests: ~$1.00
- 1000 tests: ~$10.00

**Tips to minimize costs:**
- Use Claude 3 Haiku for simple tests ($0.25 per 1M input tokens)
- Set `max_tokens` appropriately
- Cache common responses
- Use mock LLM for logic testing

---

## 🐛 Troubleshooting

### "AccessDeniedException"
→ Enable model access in Bedrock console

### "ResourceNotFoundException"  
→ Check region is `us-east-1`

### "Connection timeout"
→ Check internet connection and AWS region

### "No module named 'boto3'"
→ Run `pip install boto3`

**Full troubleshooting**: See `BEDROCK-LOCAL-SETUP.md`

---

## 📊 Testing Workflow

```
1. Mock Testing (Free)
   ↓
2. Bedrock Testing (Local, ~$1)
   ↓
3. Orchestrator Testing (Local, ~$5)
   ↓
4. Frontend Testing (Local, ~$10)
   ↓
5. Production Deployment (AWS)
```

**Current Step**: #2 - Bedrock Testing

---

## ✅ Verification Checklist

Before proceeding:

- [ ] AWS CLI installed
- [ ] AWS credentials configured
- [ ] Bedrock model access enabled
- [ ] `test_bedrock_connection.py` passes
- [ ] Example agent works
- [ ] Ready to integrate with your agents

---

## 🆘 Need Help?

1. **Setup issues**: See `BEDROCK-LOCAL-SETUP.md`
2. **Quick commands**: See `BEDROCK-QUICK-REFERENCE.md`
3. **Connection test**: Run `python test_bedrock_connection.py`
4. **AWS issues**: Check AWS Console → Bedrock → Model access

---

## 📚 Additional Resources

- **AWS Bedrock**: https://aws.amazon.com/bedrock/
- **Claude API**: https://docs.anthropic.com/claude/
- **Boto3 Docs**: https://boto3.amazonaws.com/
- **IAM Permissions**: https://docs.aws.amazon.com/bedrock/latest/userguide/security-iam.html

---

## 🎉 Ready to Start?

```cmd
# 1. Configure AWS
aws configure

# 2. Test connection
python test_bedrock_connection.py

# 3. Test example agent
python agents/aws_solutions_architect_bedrock.py
```

**That's it!** You're now testing with real Claude via Bedrock.

---

**Status**: ✅ Ready to use  
**Time to setup**: 15 minutes  
**Cost**: ~$0.10-1.00 for testing  
**Next**: Integrate with your agents
