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

### 4. Start Backend

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
