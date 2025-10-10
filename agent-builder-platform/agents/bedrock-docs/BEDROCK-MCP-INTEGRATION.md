# Bedrock + MCP Integration Guide

**How to use Bedrock Claude with your MCPs for accurate, knowledge-enhanced responses**

---

## 🎯 The Simple Truth

**Bedrock doesn't directly "connect" to MCPs.**

Instead, you:
1. Query your MCPs for knowledge
2. Include that knowledge in the prompt to Bedrock
3. Bedrock uses that knowledge to generate better responses

It's that simple!

---

## 🔄 How It Works

### The Flow

```
User Question
    ↓
Your Agent
    ↓
1. Query MCPs for relevant info
   (AWS docs, pricing, best practices)
    ↓
2. Build prompt with MCP knowledge
    ↓
3. Send to Bedrock Claude
    ↓
4. Claude generates response
   (using MCP knowledge as context)
    ↓
Response to User
```

### Code Example

```python
from agents.bedrock_llm import get_bedrock_llm

async def consult_with_mcps(user_question):
    # 1. Get MCP knowledge (you already have this)
    mcp_knowledge = """
    AWS Lambda:
    - Serverless compute
    - $0.20 per 1M requests
    - Free tier: 1M requests/month
    
    DynamoDB:
    - NoSQL database
    - $1.25 per million writes
    - Free tier: 25 GB storage
    """
    
    # 2. Build system prompt with MCP knowledge
    system_prompt = f"""You are an AWS expert.
    
    Use this AWS knowledge to answer:
    {mcp_knowledge}
    
    Provide specific, accurate recommendations."""
    
    # 3. Get Bedrock response
    bedrock = get_bedrock_llm()
    response = await bedrock.generate_response(
        prompt=user_question,
        system_prompt=system_prompt  # ← MCP knowledge here!
    )
    
    return response
```

---

## 🧪 Test It Now

```cmd
cd agent-builder-platform
python test_bedrock_with_mcps.py
```

This will show you:
1. ✅ Bedrock without MCPs (baseline)
2. ✅ Bedrock with MCP knowledge (enhanced)
3. ✅ Comparison of results

---

## 📝 Integration Pattern

### Step 1: Query Your MCPs

```python
# Your existing MCP code
mcp_ecosystem = MCPEcosystem()
mcp_ecosystem.initialize()

# Query for AWS Lambda info
lambda_info = mcp_ecosystem.query("AWS Lambda pricing")
```

### Step 2: Format MCP Knowledge

```python
def format_mcp_knowledge(mcp_results):
    """Format MCP results for Bedrock prompt"""
    
    knowledge = []
    for result in mcp_results:
        knowledge.append(f"""
{result['service']}:
- {result['description']}
- Cost: {result['pricing']}
- Best for: {result['use_cases']}
""")
    
    return "\n".join(knowledge)
```

### Step 3: Include in Bedrock Prompt

```python
async def consult(self, user_input):
    # Get MCP knowledge
    mcp_results = self.query_mcps(user_input)
    mcp_knowledge = self.format_mcp_knowledge(mcp_results)
    
    # Build system prompt
    system_prompt = f"""You are an AWS Solutions Architect.
    
    AWS Services Knowledge:
    {mcp_knowledge}
    
    Use this knowledge to provide accurate recommendations."""
    
    # Get Bedrock response
    response = await self.llm.generate_response(
        prompt=user_input,
        system_prompt=system_prompt
    )
    
    return response
```

---

## 🎓 Complete Example

Here's a full agent with Bedrock + MCP integration:

```python
from agents.bedrock_llm import get_bedrock_llm
from mcp_integration.mcp_ecosystem import MCPEcosystem

class AWSArchitectWithMCPs:
    """AWS Solutions Architect using Bedrock + MCPs"""
    
    def __init__(self):
        # Initialize Bedrock
        self.llm = get_bedrock_llm()
        
        # Initialize MCPs
        self.mcps = MCPEcosystem()
        self.mcps.initialize()
    
    async def consult(self, use_case, requirements, budget):
        """Provide consultation using Bedrock + MCP knowledge"""
        
        # 1. Query MCPs for relevant AWS services
        mcp_knowledge = await self._query_mcps(use_case, requirements)
        
        # 2. Build system prompt with MCP knowledge
        system_prompt = self._build_system_prompt(mcp_knowledge)
        
        # 3. Build user prompt
        user_prompt = self._build_user_prompt(use_case, requirements, budget)
        
        # 4. Get Bedrock response (with MCP knowledge)
        response = await self.llm.generate_response(
            prompt=user_prompt,
            system_prompt=system_prompt,
            max_tokens=3000
        )
        
        return response
    
    async def _query_mcps(self, use_case, requirements):
        """Query MCPs for relevant knowledge"""
        
        # Query AWS docs MCP
        aws_docs = self.mcps.query_mcp(
            "aws_documentation",
            f"Services for {use_case}"
        )
        
        # Query pricing MCP
        pricing = self.mcps.query_mcp(
            "aws_pricing",
            f"Cost estimates for {', '.join(requirements)}"
        )
        
        # Query Well-Architected MCP
        best_practices = self.mcps.query_mcp(
            "aws_well_architected",
            f"Best practices for {use_case}"
        )
        
        return {
            'docs': aws_docs,
            'pricing': pricing,
            'best_practices': best_practices
        }
    
    def _build_system_prompt(self, mcp_knowledge):
        """Build system prompt with MCP knowledge"""
        
        return f"""You are an expert AWS Solutions Architect.

AWS Documentation:
{mcp_knowledge['docs']}

Pricing Information:
{mcp_knowledge['pricing']}

Best Practices:
{mcp_knowledge['best_practices']}

Use this knowledge to provide accurate, specific recommendations with cost estimates."""
    
    def _build_user_prompt(self, use_case, requirements, budget):
        """Build user prompt"""
        
        reqs = "\n".join([f"- {r}" for r in requirements])
        
        return f"""Use Case: {use_case}

Requirements:
{reqs}

Budget: {budget}

Please recommend AWS services with cost breakdown."""
```

---

## ✅ What You Need

### Already Have
- ✅ Bedrock LLM service (`agents/bedrock_llm.py`)
- ✅ MCP ecosystem (`mcp-integration/mcp_ecosystem.py`)
- ✅ 16 MCPs configured

### Need to Add
- 🔄 MCP query methods in your agents
- 🔄 Prompt building with MCP knowledge
- 🔄 Integration in orchestrator

---

## 🚀 Quick Start

### Test Bedrock + MCPs Now

```cmd
# 1. Test Bedrock connection
python test_bedrock_connection.py

# 2. Test Bedrock with MCP knowledge
python test_bedrock_with_mcps.py

# 3. See the difference!
```

### Integrate into Your Agent

```python
# Add to your agent
from agents.bedrock_llm import get_bedrock_llm

class YourAgent:
    def __init__(self):
        self.llm = get_bedrock_llm()
        # Your MCP code here
    
    async def consult(self, user_input):
        # 1. Query MCPs
        mcp_knowledge = self.get_mcp_knowledge(user_input)
        
        # 2. Build prompt with MCP knowledge
        system_prompt = f"You are an expert. Use this knowledge: {mcp_knowledge}"
        
        # 3. Get Bedrock response
        response = await self.llm.generate_response(
            prompt=user_input,
            system_prompt=system_prompt
        )
        
        return response
```

---

## 💡 Key Points

### ✅ Do This
- Query MCPs for relevant knowledge
- Include MCP data in system prompts
- Let Bedrock use that knowledge
- Test with `test_bedrock_with_mcps.py`

### ❌ Don't Do This
- Try to "connect" Bedrock to MCPs directly
- Send MCP data separately from prompts
- Expect Bedrock to query MCPs itself

---

## 🎯 Benefits

**Without MCPs:**
- Generic AWS knowledge
- No specific costs
- May be outdated

**With MCPs:**
- ✅ Accurate, up-to-date info
- ✅ Real cost estimates
- ✅ Specific best practices
- ✅ Higher confidence
- ✅ Better recommendations

---

## 📊 Testing Results

Run `python test_bedrock_with_mcps.py` to see:

**Test 1: Bedrock Only**
- Generic recommendations
- No specific costs
- Basic AWS knowledge

**Test 2: Bedrock + MCP Knowledge**
- Specific services recommended
- Accurate cost breakdown
- Best practices included
- Much better quality!

---

## 🆘 Troubleshooting

### "MCPs not working"
→ MCPs work fine! Just include their knowledge in prompts

### "How do I connect them?"
→ You don't! Query MCPs, then send knowledge to Bedrock

### "Bedrock doesn't see MCP data"
→ Make sure MCP knowledge is in the `system_prompt` parameter

---

## ✅ Success Checklist

- [ ] Bedrock connection works
- [ ] Can query MCPs for knowledge
- [ ] Can include MCP knowledge in prompts
- [ ] Bedrock generates better responses with MCP data
- [ ] Tested with `test_bedrock_with_mcps.py`

---

**Ready to test?** Run `python test_bedrock_with_mcps.py` now!
