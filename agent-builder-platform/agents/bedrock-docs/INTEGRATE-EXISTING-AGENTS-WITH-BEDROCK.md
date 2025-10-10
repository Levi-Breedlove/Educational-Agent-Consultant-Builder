# Integrate Your Existing Agents with Bedrock Claude

**Step-by-step guide to connect your current agents to AWS Bedrock for local testing**

---

## 🎯 Goal

Connect your 5 existing agents to AWS Bedrock Claude so they can:
- Generate real AI responses (not hardcoded logic)
- Use their knowledge bases with Claude
- Test locally before deployment
- Maintain their existing structure and logic

---

## 📋 Prerequisites

Before starting:
- ✅ AWS credentials configured (`aws configure`)
- ✅ Bedrock model access enabled (Claude 3 Sonnet)
- ✅ Connection test passed (`python test_bedrock_connection.py`)
- ✅ Virtual environment activated

---

## 🏗️ Your Current Agent Structure

Your agents currently have:
- ✅ Knowledge bases (AWS services, patterns, best practices)
- ✅ Reasoning engines (confidence scoring, validation)
- ✅ Data structures (dataclasses, enums)
- ❌ No LLM integration (they don't "talk" yet)

**What we'll add**: LLM integration to make them conversational

---

## 🔧 Integration Pattern

### Current Agent Flow
```
User Input → Agent Logic → Hardcoded Response
```

### New Agent Flow with Bedrock
```
User Input → Agent Logic → Build Prompt → Bedrock Claude → AI Response
```

---

## 📝 Step-by-Step Integration

### Step 1: Import Bedrock LLM Service

Add to the top of your agent file:

```python
# Add this import at the top
from agents.bedrock_llm import get_bedrock_llm
```

**Example for `aws_solutions_architect.py`:**

```python
#!/usr/bin/env python3
"""
AWS Solutions Architect Agent
"""

import json
import logging
import asyncio
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, asdict
from enum import Enum

# ADD THIS LINE
from agents.bedrock_llm import get_bedrock_llm

# Rest of your imports...
```

---

### Step 2: Initialize LLM in Agent Class

Add LLM instance to your agent's `__init__` method:

```python
class AWSolutionsArchitect:
    """AWS Solutions Architect Agent"""
    
    def __init__(self):
        # Your existing initialization
        self.knowledge = AWSServicesKnowledge()
        
        # ADD THIS LINE
        self.llm = get_bedrock_llm()
        
        # Rest of your initialization...
```

---

### Step 3: Create Consultation Method with Bedrock

Add a new method that uses Bedrock for consultations:

```python
async def consult_with_bedrock(
    self,
    use_case: str,
    requirements: List[str],
    budget: str,
    experience_level: str = "beginner"
) -> Dict[str, Any]:
    """
    Provide AWS architecture consultation using Bedrock Claude
    
    Args:
        use_case: User's use case description
        requirements: List of requirements
        budget: Monthly budget
        experience_level: User's experience level
        
    Returns:
        Consultation response with recommendations
    """
    
    # Build system prompt using your knowledge base
    system_prompt = self._build_system_prompt(experience_level)
    
    # Build user prompt with context
    user_prompt = self._build_user_prompt(
        use_case, 
        requirements, 
        budget, 
        experience_level
    )
    
    # Get response from Claude
    logger.info(f"🤖 Consulting with Claude...")
    
    response = await self.llm.generate_response(
        prompt=user_prompt,
        system_prompt=system_prompt,
        max_tokens=3000,
        temperature=0.7
    )
    
    return {
        "agent": "AWS Solutions Architect",
        "response": response,
        "use_case": use_case,
        "budget": budget,
        "confidence": self._extract_confidence(response)
    }
```

---

### Step 4: Build System Prompt (Use Your Knowledge)

Create a method that builds the system prompt using your agent's knowledge:

```python
def _build_system_prompt(self, experience_level: str) -> str:
    """Build system prompt using agent's knowledge base"""
    
    # Use your existing knowledge base
    services_info = self._get_relevant_services_info()
    
    system_prompt = f"""You are an expert AWS Solutions Architect with deep knowledge of AWS services.

Your expertise includes:
- AWS service selection and architecture design
- Cost estimation and optimization
- Security best practices
- Scalability and performance
- Well-Architected Framework principles

User Experience Level: {experience_level}

Available AWS Services Knowledge:
{services_info}

Your role:
1. Recommend appropriate AWS services based on requirements
2. Provide accurate cost estimates (monthly)
3. Explain security best practices
4. Consider scalability and performance
5. Adapt explanations to user's experience level

Response Format:
1. **Recommended AWS Services** (with explanations)
2. **Architecture Overview** (how services connect)
3. **Cost Estimate** (itemized, monthly)
4. **Security Recommendations** (specific to use case)
5. **Scalability Considerations** (how it scales)
6. **Confidence Score** (0-100%)

Be concise but thorough. For beginners, explain AWS concepts. For experts, focus on optimizations."""

    return system_prompt

def _get_relevant_services_info(self) -> str:
    """Extract relevant service info from knowledge base"""
    
    # Use your existing AWSServicesKnowledge
    services = []
    for service_key, service_data in self.knowledge.services.items():
        services.append(f"- {service_data['name']}: {service_data['description']}")
    
    return "\n".join(services[:10])  # Top 10 most relevant
```

---

### Step 5: Build User Prompt

Create a method that formats the user's input:

```python
def _build_user_prompt(
    self,
    use_case: str,
    requirements: List[str],
    budget: str,
    experience_level: str
) -> str:
    """Build user prompt with all context"""
    
    requirements_text = "\n".join([f"- {req}" for req in requirements])
    
    user_prompt = f"""Use Case: {use_case}

Requirements:
{requirements_text}

Budget: {budget}
Experience Level: {experience_level}

Please provide AWS architecture recommendations that:
1. Meet all requirements
2. Stay within budget
3. Follow AWS best practices
4. Are appropriate for my experience level

Include specific AWS services, cost breakdown, and security recommendations."""

    return user_prompt
```

---

### Step 6: Extract Confidence Score

Add a helper to extract confidence from Claude's response:

```python
def _extract_confidence(self, response: str) -> float:
    """Extract confidence score from response"""
    
    # Look for confidence score in response
    import re
    match = re.search(r'confidence[:\s]+(\d+)%', response.lower())
    
    if match:
        return float(match.group(1)) / 100.0
    
    # Default to high confidence if Claude responded
    return 0.95
```

---

## 🧪 Complete Example: AWS Solutions Architect

Here's a complete integration example:

```python
#!/usr/bin/env python3
"""
AWS Solutions Architect Agent with Bedrock Integration
"""

import json
import logging
import asyncio
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from enum import Enum
import re

# Import Bedrock LLM
from agents.bedrock_llm import get_bedrock_llm

logger = logging.getLogger(__name__)

class ExperienceLevel(Enum):
    BEGINNER = "beginner"
    INTERMEDIATE = "intermediate"
    ADVANCED = "advanced"
    EXPERT = "expert"

class AWSolutionsArchitect:
    """AWS Solutions Architect with Bedrock Claude integration"""
    
    def __init__(self):
        # Your existing knowledge base
        self.knowledge = AWSServicesKnowledge()
        
        # Add Bedrock LLM
        self.llm = get_bedrock_llm()
        
        self.agent_name = "AWS Solutions Architect"
    
    async def consult(
        self,
        use_case: str,
        requirements: List[str],
        budget: str,
        experience_level: str = "beginner"
    ) -> Dict[str, Any]:
        """Main consultation method using Bedrock"""
        
        # Build prompts
        system_prompt = self._build_system_prompt(experience_level)
        user_prompt = self._build_user_prompt(
            use_case, requirements, budget, experience_level
        )
        
        # Get Claude's response
        logger.info(f"🤖 {self.agent_name} consulting with Claude...")
        
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
            "confidence": self._extract_confidence(response)
        }
    
    def _build_system_prompt(self, experience_level: str) -> str:
        """Build system prompt with knowledge base"""
        
        services_info = self._get_services_summary()
        
        return f"""You are an expert AWS Solutions Architect.

User Experience: {experience_level}

AWS Services Available:
{services_info}

Provide recommendations in this format:
1. Recommended Services (with explanations)
2. Architecture Overview
3. Cost Estimate (monthly, itemized)
4. Security Best Practices
5. Scalability Considerations
6. Confidence Score (0-100%)

Adapt explanations to user's experience level."""
    
    def _build_user_prompt(
        self, use_case, requirements, budget, experience_level
    ) -> str:
        """Build user prompt"""
        
        reqs = "\n".join([f"- {r}" for r in requirements])
        
        return f"""Use Case: {use_case}

Requirements:
{reqs}

Budget: {budget}

Provide AWS architecture recommendations."""
    
    def _get_services_summary(self) -> str:
        """Get summary of AWS services from knowledge base"""
        
        services = []
        for key, data in self.knowledge.services.items():
            services.append(f"- {data['name']}: {data['description']}")
        
        return "\n".join(services[:10])
    
    def _extract_confidence(self, response: str) -> float:
        """Extract confidence from response"""
        
        match = re.search(r'confidence[:\s]+(\d+)%', response.lower())
        return float(match.group(1)) / 100.0 if match else 0.95

# Your existing AWSServicesKnowledge class stays the same
class AWSServicesKnowledge:
    # ... your existing code ...
    pass
```

---

## 🧪 Test Your Integrated Agent

Create a test file `test_my_agent_bedrock.py`:

```python
"""
Test your agent with Bedrock
"""

import asyncio
import logging
from agents.aws_solutions_architect import AWSolutionsArchitect

logging.basicConfig(level=logging.INFO)

async def test_agent():
    print("\n" + "="*60)
    print("🧪 Testing AWS Solutions Architect with Bedrock")
    print("="*60 + "\n")
    
    # Create agent
    agent = AWSolutionsArchitect()
    
    # Test consultation
    result = await agent.consult(
        use_case="Build a chatbot for customer support",
        requirements=[
            "Handle 1000 requests per day",
            "Store conversation history",
            "Integrate with CRM"
        ],
        budget="$50/month",
        experience_level="beginner"
    )
    
    print(f"Agent: {result['agent']}")
    print(f"Confidence: {result['confidence']:.0%}")
    print("\nResponse:")
    print("-" * 60)
    print(result['response'])
    print("-" * 60 + "\n")

if __name__ == "__main__":
    asyncio.run(test_agent())
```

**Run the test:**
```cmd
python test_my_agent_bedrock.py
```

---

## 🔄 Integration Checklist for All 5 Agents

Apply this pattern to each agent:

### ✅ Agent 1: AWS Solutions Architect
- [ ] Import `get_bedrock_llm()`
- [ ] Add `self.llm` to `__init__`
- [ ] Create `consult()` method
- [ ] Build system prompt with knowledge
- [ ] Test with Bedrock

### ✅ Agent 2: Architecture Advisor
- [ ] Import `get_bedrock_llm()`
- [ ] Add `self.llm` to `__init__`
- [ ] Create `review_architecture()` method
- [ ] Include Well-Architected principles
- [ ] Test with Bedrock

### ✅ Agent 3: Implementation Guide
- [ ] Import `get_bedrock_llm()`
- [ ] Add `self.llm` to `__init__`
- [ ] Create `generate_code()` method
- [ ] Include code generation context
- [ ] Test with Bedrock

### ✅ Agent 4: Testing Validator
- [ ] Import `get_bedrock_llm()`
- [ ] Add `self.llm` to `__init__`
- [ ] Create `validate()` method
- [ ] Include security/performance checks
- [ ] Test with Bedrock

### ✅ Agent 5: Strands Integration
- [ ] Import `get_bedrock_llm()`
- [ ] Add `self.llm` to `__init__`
- [ ] Create `export_spec()` method
- [ ] Include Strands patterns
- [ ] Test with Bedrock

---

## 💡 Best Practices

### 1. Use Your Knowledge Bases
```python
# Include your existing knowledge in system prompts
system_prompt = f"""You are an expert with this knowledge:

{self.knowledge.get_relevant_info()}

Use this knowledge to provide accurate recommendations."""
```

### 2. Maintain Confidence Scoring
```python
# Extract and use confidence scores
confidence = self._extract_confidence(response)

if confidence < 0.90:
    logger.warning(f"Low confidence: {confidence:.0%}")
```

### 3. Handle Errors Gracefully
```python
try:
    response = await self.llm.generate_response(...)
except Exception as e:
    logger.error(f"Bedrock error: {e}")
    return self._fallback_response()
```

### 4. Keep Existing Methods
```python
# Keep your existing methods for backward compatibility
def analyze_requirements(self, ...):
    # Your existing logic
    pass

# Add new Bedrock methods
async def consult_with_bedrock(self, ...):
    # New Bedrock integration
    pass
```

---

## 🚀 Quick Integration Template

Copy this template for each agent:

```python
from agents.bedrock_llm import get_bedrock_llm

class YourAgent:
    def __init__(self):
        # Your existing code
        self.knowledge = YourKnowledgeBase()
        
        # Add Bedrock
        self.llm = get_bedrock_llm()
    
    async def consult(self, user_input: str) -> Dict[str, Any]:
        """Main consultation method"""
        
        # Build prompts using your knowledge
        system_prompt = self._build_system_prompt()
        user_prompt = self._build_user_prompt(user_input)
        
        # Get Claude's response
        response = await self.llm.generate_response(
            prompt=user_prompt,
            system_prompt=system_prompt,
            max_tokens=3000
        )
        
        return {
            "agent": "Your Agent Name",
            "response": response
        }
    
    def _build_system_prompt(self) -> str:
        """Build system prompt with your knowledge"""
        return f"""You are an expert in [your domain].
        
Your knowledge includes:
{self.knowledge.get_summary()}

Provide expert recommendations."""
    
    def _build_user_prompt(self, user_input: str) -> str:
        """Build user prompt"""
        return f"""User Request: {user_input}

Please provide expert guidance."""
```

---

## 📊 Testing Workflow

```
1. Test Connection
   ↓ python test_bedrock_connection.py
   
2. Test Single Agent
   ↓ python test_my_agent_bedrock.py
   
3. Test All Agents
   ↓ python test_all_agents_bedrock.py
   
4. Test with Orchestrator
   ↓ python test_orchestrator_bedrock.py
   
5. Test with Frontend
   ↓ npm run dev (frontend)
```

---

## 💰 Cost Tracking

Each consultation costs approximately:
- Input: ~500 tokens × $0.003/1K = $0.0015
- Output: ~1500 tokens × $0.015/1K = $0.0225
- **Total per consultation: ~$0.024**

**100 tests = ~$2.40**

---

## 🆘 Troubleshooting

### Agent not responding
→ Check `test_bedrock_connection.py` passes

### "No module named 'bedrock_llm'"
→ Ensure `agents/bedrock_llm.py` exists

### Low quality responses
→ Improve system prompt with more context

### High costs
→ Reduce `max_tokens` or use Claude 3 Haiku

---

## ✅ Success Criteria

You're done when:
- ✅ All 5 agents have Bedrock integration
- ✅ Each agent can be tested independently
- ✅ Responses use agent's knowledge base
- ✅ Confidence scores are extracted
- ✅ Ready to integrate with orchestrator

---

## 🎯 Next Steps

After integrating all agents:

1. **Test with Orchestrator**
   - Update orchestrator to use Bedrock agents
   - Test full 5-phase workflow

2. **Connect to Frontend**
   - Update API to use Bedrock agents
   - Test through UI

3. **Optimize Prompts**
   - Refine system prompts
   - Improve response quality

4. **Deploy to AWS**
   - Follow deployment guide
   - Monitor costs and performance

---

**Ready to integrate?** Start with Agent 1 (AWS Solutions Architect) using the example above!
