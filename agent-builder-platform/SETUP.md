# Agent Builder Platform - Setup Guide

Get the Agent Builder Platform running locally in 5 minutes.

## Prerequisites

Install these first:
- **Python 3.9+** - [Download](https://www.python.org/downloads/)
- **Node.js 18+** - [Download](https://nodejs.org/)
- **Git** - [Download](https://git-scm.com/)

## Quick Start

### 1. Clone Repository
```bash
git clone https://github.com/Levi-Breedlove/Hackathon-Preview.git
cd Hackathon-Preview/agent-builder-platform
```

### 2. Run Setup Script (One-Time Setup)

```cmd
cd agent-builder-platform
.\setup.bat
```

This will:
- Create virtual environment at root level
- Install Python dependencies
- Install frontend dependencies
- Create .env file

### 3. Start the Application

**Option A: Automatic Start (Recommended)**

```cmd
cd agent-builder-platform
.\start.bat
```

This automatically opens two windows:
- **Backend**: Activates venv and runs `uvicorn api.main:app --reload`
- **Frontend**: Runs `npm run dev`

**Option B: Manual Start**

If you prefer to start servers manually:

**Terminal 1 - Backend:**
```cmd
venv\Scripts\activate.bat
cd agent-builder-platform
uvicorn api.main:app --reload
```

**Terminal 2 - Frontend:**
```cmd
cd agent-builder-platform\frontend
npm run dev
```

### 4. Access Application
- **Frontend**: http://localhost:5173
- **API Docs**: http://localhost:8000/api/docs

### 5. Validate Setup (Optional)

```cmd
cd agent-builder-platform
.\validate-infrastructure-safe.ps1
```

---

## Manual Setup (Alternative)

If the automated setup doesn't work, follow these steps:

### Backend Setup

**Windows (PowerShell):**
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

**Windows (CMD):**
```cmd
python -m venv venv
venv\Scripts\activate.bat
pip install -r requirements.txt
```

**Linux/Mac:**
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Frontend Setup
```bash
cd frontend
npm install
cd ..
```

---

## Project Structure

```
agent-builder-platform/
├── api/                    # FastAPI backend (11 endpoints)
├── frontend/               # React + TypeScript UI
├── agents/                 # 5 AI consultant agents
├── agent-core/            # Orchestration logic
├── mcp-integration/       # 16 MCP ecosystem
└── docs/                  # Documentation
```

## Key Features

- **Chat Interface** - AI consultant interaction
- **Architecture Visualization** - AWS diagrams
- **Code Preview** - Syntax highlighting with CodeMirror
- **Confidence Dashboard** - Real-time tracking
- **Export** - 5 formats (Python, CloudFormation, Terraform, Docker, Strands)

---

## Troubleshooting

### Port Already in Use
```bash
# Backend - use different port
uvicorn api.main:app --reload --port 8001

# Frontend - use different port
npm run dev -- --port 5174
```

### Module Not Found
Activate virtual environment and reinstall:
```bash
# Windows
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt

# Linux/Mac
source venv/bin/activate
pip install -r requirements.txt
```

### Import Error
Run backend from `agent-builder-platform` directory (not from `api` folder):
```bash
cd agent-builder-platform
uvicorn api.main:app --reload
```

### Frontend Issues
```bash
cd frontend
rm -rf node_modules package-lock.json
npm install
```

---

## Documentation

- **[Complete Documentation](docs/COMPLETE-DOCUMENTATION.md)** - Full system architecture
- **[Status Dashboard](docs/STATUS-DASHBOARD.md)** - Implementation progress
- **[Validation Guide](VALIDATION-GUIDE.md)** - Project structure validation

## Support

- **Issues**: [GitHub Issues](https://github.com/Levi-Breedlove/Hackathon-Preview/issues)
- **Repository**: [Hackathon-Preview](https://github.com/Levi-Breedlove/Hackathon-Preview)

---

**Note**: This is a development setup. Production deployment requires additional AWS configuration.
