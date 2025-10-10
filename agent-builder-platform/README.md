# Agent Builder Platform

**AI-Powered Teacher & Guide for Building Strands Agents on AWS**

## What It Does

**This is an educational consultation platform** that teaches you how to build production-ready AI agents using **Strands agent builder** and **AWS services** through guided conversations with 5 specialist AI consultants. Think of it as having expert mentors who:

- **Ask clarifying questions** to understand your needs
- **Explain AWS services** and how they work together
- **Walk you through Strands agent builder** step-by-step
- **Teach you AWS architecture** best practices (Well-Architected Framework)
- **Show you how to configure** action groups, knowledge bases, and guardrails
- **Explain security and cost optimization** for AWS deployments
- **Generate complete code** with explanations of what each part does

**You learn by doing** - the consultants guide you through building a Strands agent on AWS while explaining why each decision matters.

### Specifically Designed For:
- ✅ **Strands Agent Builder**: Learn to use Strands framework for agent development
- ✅ **AWS Services**: Lambda, Bedrock, DynamoDB, S3, API Gateway, etc.
- ✅ **AWS Well-Architected**: Security, reliability, performance, cost optimization
- ✅ **Production Deployment**: Real-world AWS infrastructure and monitoring

## The 5 AI Consultants (AWS & Strands Experts)

- **AWS Solutions Architect**: Teaches AWS service selection and architecture patterns
- **Architecture Advisor**: Guides you through AWS Well-Architected Framework
- **Implementation Guide**: Shows you how to write AWS SDK code and Lambda functions
- **Testing Validator**: Teaches AWS security, performance, and cost validation
- **Strands Integration**: Walks you through Strands agent builder configuration

## Current Status

**Backend: 100% Complete** | **Frontend: Not Started**

See [STATUS-DASHBOARD.md](docs/STATUS-DASHBOARD.md) for detailed progress.

## Documentation

Complete documentation: [COMPLETE-DOCUMENTATION.md](docs/COMPLETE-DOCUMENTATION.md)

## Quick Start

### 1. Clone Repository
```bash
git clone https://github.com/Levi-Breedlove/Hackathon-Preview.git
cd Hackathon-Preview/agent-builder-platform
```

### 2. Run Setup Script

**Windows (PowerShell):**
```powershell
.\setup.ps1
```

**Windows (CMD):**
```cmd
setup.bat
```

**Linux/Mac:**
```bash
chmod +x setup.sh
./setup.sh
```

### 3. Validate Setup (Optional)

**Windows:**
```powershell
.\validate-infrastructure-safe.ps1
```

**Linux/Mac:**
```bash
./validate-infrastructure-safe.sh
```

See [VALIDATION-GUIDE.md](VALIDATION-GUIDE.md) for details.

### 4. Start Backend

Make sure you're in the `agent-builder-platform` directory, then:

**Windows (PowerShell):**
```powershell
.\venv\Scripts\Activate.ps1
uvicorn api.main:app --reload
```

**Windows (CMD):**
```cmd
venv\Scripts\activate.bat
uvicorn api.main:app --reload
```

**Linux/Mac:**
```bash
source venv/bin/activate
uvicorn api.main:app --reload
```

### 5. Start Frontend (New Terminal)
```bash
cd frontend
npm run dev
```

### 6. Access Application
- **Frontend**: http://localhost:5173
- **API Docs**: http://localhost:8000/api/docs

---

**For detailed setup instructions**, see [SETUP.md](SETUP.md)

## How It Works: Guided Learning Process

**5-Phase Educational Consultation**:

1. **Requirements Phase** - AWS Solutions Architect teaches you:
   - How to identify your use case requirements
   - AWS service selection criteria
   - Cost estimation techniques
   - Security considerations

2. **Architecture Phase** - Architecture Advisor guides you through:
   - Well-Architected Framework principles
   - Design pattern selection
   - Trade-off analysis
   - Scalability planning

3. **Implementation Phase** - Implementation Guide shows you:
   - How to write production-ready code
   - Best practices for error handling
   - Testing strategies
   - Documentation standards

4. **Testing Phase** - Testing Validator teaches you:
   - Security validation techniques
   - Performance benchmarking
   - Cost optimization opportunities
   - Production readiness checks

5. **Strands Integration Phase** - Strands Integration walks you through:
   - **How to use Strands agent builder framework**
   - Translating AWS architecture to Strands specifications
   - Configuring Strands action groups with AWS Lambda
   - Setting up knowledge bases with AWS OpenSearch/Bedrock
   - Deploying Strands agents to AWS infrastructure
   - Best practices for Strands + AWS integration

**Output**: Complete Strands agent on AWS + **knowledge of how to build Strands agents on AWS yourself**

## Cost

Development: $16-30/month (AWS free tier optimized)

## Tech Stack

- Python 3.12, FastAPI
- Amazon Bedrock (Claude + Titan)
- DynamoDB, S3, Lambda
- 16 MCP ecosystem

---

**Built for AWS Agent Hackathon**
