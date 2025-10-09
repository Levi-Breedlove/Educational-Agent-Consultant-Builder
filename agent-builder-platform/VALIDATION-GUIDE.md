# Validation Guide

This guide explains how to validate your Agent Builder Platform setup before running it locally or deploying to AWS.

## Safe Validation (No AWS Access)

The `validate-infrastructure-safe.sh` script validates your project structure and configuration **without accessing AWS**. This is perfect for:
- GitHub demo testing
- Local development verification
- Pre-deployment checks
- CI/CD pipeline validation

### Running Safe Validation

```bash
# Linux/Mac
chmod +x validate-infrastructure-safe.sh
./validate-infrastructure-safe.sh

# Windows PowerShell
.\validate-infrastructure-safe.ps1

# Windows (Git Bash)
bash validate-infrastructure-safe.sh
```

### What It Checks

1. **CloudFormation Templates** - YAML syntax and required sections
2. **Agent Core Configuration** - YAML syntax and agent definitions
3. **Deployment Scripts** - Existence and executability
4. **Documentation** - Key documentation files
5. **Project Structure** - All required directories
6. **Setup Files** - Setup scripts and configuration files
7. **Python Agent Files** - All 5 AI consultant agents
8. **API Files** - FastAPI backend components
9. **Frontend Files** - React UI components

### Expected Output

```
🛡️  Safe Infrastructure Validation (No AWS Access)
====================================================

This validation runs completely offline - no AWS charges possible!

📋 Test 1: CloudFormation Template Syntax...
✅ CloudFormation template has valid YAML syntax
✅ CloudFormation template has proper format version
✅ CloudFormation template has Resources section

🤖 Test 2: Agent Core Configuration...
✅ Agent Core configuration has valid YAML syntax
✅ Agent Core configuration has agents section

📜 Test 3: Deployment Scripts...
✅ deploy-infrastructure.sh exists and is executable
✅ test-aws-connectivity.sh exists and is executable
✅ validate-config.sh exists and is executable
✅ deploy-mcp-integration.sh exists and is executable
✅ deploy-frontend.sh exists and is executable

📚 Test 4: Documentation...
✅ SETUP.md exists
✅ README.md exists
✅ INDEX.md exists
✅ COMPLETE-DOCUMENTATION.md exists
✅ STATUS-DASHBOARD.md exists

🏗️  Test 5: Project Structure...
✅ infrastructure/ directory exists
✅ agent-core/ directory exists
✅ agent-core-config/ directory exists
✅ agents/ directory exists
✅ api/ directory exists
✅ frontend/ directory exists
✅ mcp-integration/ directory exists
✅ scripts/ directory exists
✅ docs/ directory exists
✅ agent-builder-platform/ directory exists

⚙️  Test 6: Setup Files...
✅ setup.sh exists
✅ setup.ps1 exists
✅ requirements.txt exists
✅ .env.example exists
✅ package.json exists

🐍 Test 7: Python Agent Files...
✅ aws_solutions_architect.py exists
✅ architecture_advisor.py exists
✅ implementation_guide.py exists
✅ testing_validator.py exists
✅ strands_builder_integration.py exists

🌐 Test 8: API Files...
✅ main.py exists
✅ workflow_service.py exists
✅ session_service.py exists
✅ export_service.py exists
✅ websocket_service.py exists

⚛️  Test 9: Frontend Files...
✅ frontend/src/ directory exists
✅ HomePage.tsx exists
✅ AgentBuilderPage.tsx exists
✅ vite.config.ts exists

🎯 Validation Summary:
==============================
✅ All critical validations passed!

📊 Project Status:
  • Infrastructure: ✅ Ready
  • Backend API: ✅ Ready
  • Frontend UI: ✅ Ready
  • 5 AI Agents: ✅ Ready
  • 16 MCPs: ✅ Configured
  • Documentation: ✅ Complete

🚀 Ready for Local Demo!
💰 Current cost: $0.00 (no AWS resources created)

Next Steps for GitHub Demo:
1. Run setup script:
   • Windows: .\setup.ps1
   • Linux/Mac: ./setup.sh

2. Start backend API:
   • cd api
   • uvicorn main:app --reload

3. Start frontend (new terminal):
   • cd frontend
   • npm run dev

4. Open browser: http://localhost:5173

🛡️  No AWS credentials needed for local demo!
```

## AWS Validation (Requires AWS Access)

The `scripts/validate-config.sh` script performs comprehensive validation **including AWS connectivity checks**. Use this when:
- Preparing for AWS deployment
- Validating AWS credentials
- Checking Bedrock access
- Verifying CloudFormation templates with AWS

### Running AWS Validation

```bash
# Set AWS credentials first
export AWS_REGION=us-east-1
export AWS_ACCOUNT_ID=123456789012
export GITHUB_TOKEN=ghp_your_token_here

# Run validation
cd agent-builder-platform
./scripts/validate-config.sh
```

### What It Checks

1. **Environment Variables** - Required AWS configuration
2. **AWS Connectivity** - Valid credentials and account access
3. **Bedrock Access** - Claude 3 Haiku model availability
4. **CloudFormation Template** - AWS validation
5. **Agent Core Configuration** - Complete agent setup
6. **Project Structure** - All required files
7. **Deployment Readiness** - Scripts and configuration

### Expected Output

```
🔍 Agent Builder Platform - Configuration Validation
====================================================

[VALIDATE] Validating project structure...
✅ Directory exists: infrastructure
✅ Directory exists: agent-core-config
✅ Directory exists: scripts
✅ File exists: README.md
✅ File exists: infrastructure/main-stack.yaml
✅ File exists: agent-core-config/config.yaml
✅ File exists: scripts/deploy-infrastructure.sh

[VALIDATE] Validating environment variables...
✅ Environment variable AWS_REGION is set
✅ Environment variable AWS_ACCOUNT_ID is set
✅ Environment variable GITHUB_TOKEN is set
✅ AWS_REGION format is valid: us-east-1
✅ AWS_ACCOUNT_ID format is valid

[VALIDATE] Validating AWS connectivity...
✅ AWS credentials are valid
[VALIDATE] Connected as: arn:aws:iam::123456789012:user/demo-user
[VALIDATE] Account ID: 123456789012

[VALIDATE] Validating Bedrock access...
✅ Bedrock access is available
✅ Claude 3 Haiku model is available

[VALIDATE] Validating CloudFormation template...
✅ CloudFormation template is valid

[VALIDATE] Validating Agent Core configuration...
✅ Configuration section found: agents:
✅ Configuration section found: mcps:
✅ Configuration section found: tools:
✅ Configuration section found: monitoring:
✅ Expert consultant configured: orchestrator:
✅ Expert consultant configured: requirements-analyst:
✅ Expert consultant configured: architecture-advisor:
✅ Expert consultant configured: implementation-guide:
✅ Expert consultant configured: testing-validator:

[VALIDATE] Validating deployment readiness...
✅ Deployment script is executable
✅ No stale .env file found

🔍 Configuration Validation Report
==================================

✅ All critical validations passed!
✅ No warnings found

📊 Validation Summary:
  • Errors: 0
  • Warnings: 0

✅ Configuration is ready for deployment!

🚀 Next Steps:
  1. Run './scripts/deploy-infrastructure.sh' to deploy AWS infrastructure
  2. Monitor costs using AWS Billing Dashboard
  3. Proceed with Task 2: MCP integrations and knowledge synchronization
```

## Troubleshooting

### Python Not Found

```bash
# Install Python 3.9+
# Windows: Download from https://www.python.org/
# Mac: brew install python3
# Linux: sudo apt-get install python3
```

### Node.js Not Found

```bash
# Install Node.js 18+
# Windows: Download from https://nodejs.org/
# Mac: brew install node
# Linux: sudo apt-get install nodejs npm
```

### Script Not Executable

```bash
# Make script executable
chmod +x validate-infrastructure-safe.sh
chmod +x agent-builder-platform/scripts/*.sh
```

### YAML Validation Fails

```bash
# Install PyYAML
pip install pyyaml

# Or use Python virtual environment
source venv/bin/activate  # Linux/Mac
.\venv\Scripts\Activate.ps1  # Windows
pip install pyyaml
```

### AWS Credentials Invalid

```bash
# Configure AWS CLI
aws configure

# Or set environment variables
export AWS_ACCESS_KEY_ID=your_access_key
export AWS_SECRET_ACCESS_KEY=your_secret_key
export AWS_REGION=us-east-1
```

## Validation Checklist

Before running the application:

- [ ] Run `validate-infrastructure-safe.sh` - All tests pass
- [ ] Run setup script (`setup.sh` or `setup.ps1`)
- [ ] Python virtual environment created
- [ ] Python dependencies installed
- [ ] Frontend dependencies installed
- [ ] `.env` file created (optional for demo)

Before AWS deployment:

- [ ] Run `scripts/validate-config.sh` - All tests pass
- [ ] AWS credentials configured
- [ ] Bedrock access verified
- [ ] CloudFormation template validated
- [ ] Cost monitoring enabled
- [ ] GitHub token configured (for MCP)

## Cost Safety

### Local Demo (No AWS)
- **Cost**: $0.00
- **No AWS credentials needed**
- **No AWS resources created**
- **Safe for GitHub demos**

### AWS Deployment
- **Estimated Cost**: $16-30 total
- **Requires AWS credentials**
- **Creates AWS resources**
- **Monitor costs in AWS Billing Dashboard**

## Support

- **Documentation**: [docs/INDEX.md](docs/INDEX.md)
- **Setup Guide**: [SETUP.md](SETUP.md)
- **Architecture**: [docs/COMPLETE-DOCUMENTATION.md](docs/COMPLETE-DOCUMENTATION.md)
- **Issues**: Create an issue on GitHub

---

**Note**: Always run `validate-infrastructure-safe.sh` before local demos to ensure your project structure is correct without accessing AWS.
