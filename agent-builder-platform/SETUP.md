# Agent Builder Platform - Setup Guide

Quick setup guide to get the Agent Builder Platform running locally for demo purposes.

## Prerequisites

- **Python 3.9+** - [Download Python](https://www.python.org/downloads/)
- **Node.js 18+** - [Download Node.js](https://nodejs.org/)
- **Git** - [Download Git](https://git-scm.com/)

## Validation (Optional but Recommended)

Before setup, you can validate your project structure:

#### Windows PowerShell:
```powershell
.\validate-infrastructure-safe.ps1
```

#### Linux/Mac:
```bash
chmod +x validate-infrastructure-safe.sh
./validate-infrastructure-safe.sh
```

This validates your project structure **without accessing AWS** (completely safe, $0 cost).

See [VALIDATION-GUIDE.md](VALIDATION-GUIDE.md) for details.

## Quick Start (5 minutes)

### Complete Setup Steps

#### Step 1: Clone Repository (if from GitHub)
```bash
git clone <your-repo-url>
cd agent-builder-platform
```

#### Step 2: Run Setup Script

**Windows PowerShell:**
```powershell
.\setup.ps1
```

**Windows Command Prompt (CMD):**
```cmd
setup.bat
```

**Linux/Mac:**
```bash
chmod +x setup.sh
./setup.sh
```

#### Step 3: Start Backend

**Windows PowerShell:**
```powershell
.\venv\Scripts\Activate.ps1
uvicorn api.main:app --reload
```

**Windows CMD:**
```cmd
venv\Scripts\activate.bat
uvicorn api.main:app --reload
```

**Linux/Mac:**
```bash
source venv/bin/activate
uvicorn api.main:app --reload
```

#### Step 4: Start Frontend (New Terminal)
```bash
cd frontend
npm run dev
```

#### Step 5: Open Browser
- Frontend: http://localhost:5173
- API Docs: http://localhost:8000/api/docs

---

### Option 1: Automated Setup (Recommended)

#### Windows PowerShell:
```powershell
.\setup.ps1
```

#### Windows Command Prompt (CMD):
```cmd
setup.bat
```

#### Linux/Mac:
```bash
chmod +x setup.sh
./setup.sh
```

### Option 2: Manual Setup

#### 1. Clone the Repository
```bash
git clone <your-repo-url>
cd agent-builder-platform
```

#### 2. Backend Setup
```bash
# Create Python virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
.\venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Install Python dependencies
pip install -r requirements.txt
```

#### 3. Frontend Setup
```bash
cd frontend
npm install
cd ..
```

#### 4. Environment Configuration
```bash
# Copy example environment file
cp .env.example .env

# Edit .env with your configuration (optional for demo)
```

## Running the Application

### Start Backend API

**Important**: Run the backend from the `agent-builder-platform` directory (not from inside `api`).

#### Windows PowerShell:
```powershell
# Activate virtual environment
.\venv\Scripts\Activate.ps1

# Start backend (from agent-builder-platform directory)
uvicorn api.main:app --reload
```

#### Windows CMD:
```cmd
REM Activate virtual environment
venv\Scripts\activate.bat

REM Start backend (from agent-builder-platform directory)
uvicorn api.main:app --reload
```

#### Linux/Mac:
```bash
# Activate virtual environment
source venv/bin/activate

# Start backend (from agent-builder-platform directory)
uvicorn api.main:app --reload
```

### Start Frontend (in a new terminal)
```bash
cd frontend
npm run dev
```

### Access the Application
- **Frontend**: http://localhost:5173
- **API Docs**: http://localhost:8000/api/docs
- **API ReDoc**: http://localhost:8000/api/redoc

## Running Tests

### Windows:
```cmd
run_comprehensive_tests.bat
```

### Linux/Mac:
```bash
# Activate virtual environment
source venv/bin/activate

# Run tests
cd api
python run_all_tests.py
```

## Demo Mode

The application includes mock data for demonstration purposes:
- Confidence scores are pre-populated
- Workflow phases can be controlled via Dev Tools panel
- No AWS credentials required for UI demo

## Architecture Overview

```
agent-builder-platform/
├── api/                    # FastAPI backend (11 endpoints)
├── frontend/               # React + TypeScript UI
├── agents/                 # 5 AI consultant agents
├── agent-core/            # Orchestration logic
├── mcp-integration/       # 16 MCP ecosystem
├── infrastructure/        # AWS CloudFormation templates
└── docs/                  # Documentation
```

## Key Features to Demo

1. **Home Page** - Dark theme with responsive design
2. **Chat Interface** - AI consultant interaction
3. **Architecture Tab** - AWS architecture visualization
4. **Code Tab** - Generated code preview with syntax highlighting
5. **Confidence Tab** - Real-time confidence tracking with charts
6. **Dev Tools Panel** - Draggable workflow controls (dev mode only)

## Troubleshooting

### Port Already in Use

#### Backend (change port):
```bash
# Use port 8001 instead
uvicorn api.main:app --reload --port 8001
```

#### Frontend (change port):
```bash
# Use port 5174 instead
npm run dev -- --port 5174
```

### Python Module Not Found

Make sure virtual environment is activated:

#### Windows PowerShell:
```powershell
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

#### Windows CMD:
```cmd
venv\Scripts\activate.bat
pip install -r requirements.txt
```

#### Linux/Mac:
```bash
source venv/bin/activate
pip install -r requirements.txt
```

### Import Error: "attempted relative import with no known parent package"

This means you're trying to run the backend from inside the `api` directory. **Solution**: Run from the `agent-builder-platform` directory:

```bash
# Make sure you're in agent-builder-platform directory
cd agent-builder-platform

# Then run
uvicorn api.main:app --reload
```

### Node Modules Issues

#### Windows CMD:
```cmd
cd frontend
rmdir /s /q node_modules
del package-lock.json
npm install
```

#### Windows PowerShell:
```powershell
cd frontend
Remove-Item -Recurse -Force node_modules
Remove-Item package-lock.json
npm install
```

#### Linux/Mac:
```bash
cd frontend
rm -rf node_modules package-lock.json
npm install
```

### Virtual Environment Not Found

If `venv` doesn't exist, run the setup script again:

#### Windows:
```cmd
setup.bat
```

#### Linux/Mac:
```bash
./setup.sh
```

## Production Deployment

For production deployment, see:
- [Deployment Guide](docs/guides/deployment-guide.md)
- [AWS Infrastructure Setup](infrastructure/README.md)
- [Security Configuration](docs/security-compliance.md)

## Support

- **Documentation**: [docs/INDEX.md](docs/INDEX.md)
- **Issues**: Create an issue on GitHub
- **Architecture**: [docs/COMPLETE-DOCUMENTATION.md](docs/COMPLETE-DOCUMENTATION.md)

## License

[Your License Here]

---

**Note**: This is a demo/development setup. For production deployment, additional configuration for AWS services, security, and monitoring is required.
