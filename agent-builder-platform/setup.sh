#!/bin/bash
# Agent Builder Platform - Linux/Mac Setup Script
# This script automates the setup process for Linux and macOS

echo "🚀 Agent Builder Platform - Automated Setup"
echo "============================================="
echo ""

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

SETUP_ERRORS=0

# Check Python installation
echo -e "${YELLOW}📋 Checking prerequisites...${NC}"
if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 --version)
    echo -e "${GREEN}✅ Python found: $PYTHON_VERSION${NC}"
    PYTHON_CMD="python3"
elif command -v python &> /dev/null; then
    PYTHON_VERSION=$(python --version)
    echo -e "${GREEN}✅ Python found: $PYTHON_VERSION${NC}"
    PYTHON_CMD="python"
else
    echo -e "${RED}❌ Python not found. Please install Python 3.9+ from https://www.python.org/${NC}"
    ((SETUP_ERRORS++))
fi

# Check Node.js installation
if command -v node &> /dev/null; then
    NODE_VERSION=$(node --version)
    echo -e "${GREEN}✅ Node.js found: $NODE_VERSION${NC}"
else
    echo -e "${RED}❌ Node.js not found. Please install Node.js 18+ from https://nodejs.org/${NC}"
    ((SETUP_ERRORS++))
fi

# Check npm installation
if command -v npm &> /dev/null; then
    NPM_VERSION=$(npm --version)
    echo -e "${GREEN}✅ npm found: v$NPM_VERSION${NC}"
else
    echo -e "${RED}❌ npm not found. Please install Node.js 18+ (includes npm) from https://nodejs.org/${NC}"
    ((SETUP_ERRORS++))
fi

# Exit if prerequisites are missing
if [ $SETUP_ERRORS -gt 0 ]; then
    echo ""
    echo -e "${RED}❌ Setup cannot continue. Please install missing prerequisites.${NC}"
    exit 1
fi

echo ""
echo -e "${YELLOW}🐍 Setting up Python backend...${NC}"

# Create virtual environment
if [ -d "venv" ]; then
    echo -e "${YELLOW}⚠️  Virtual environment already exists. Skipping creation.${NC}"
else
    echo "Creating Python virtual environment..."
    $PYTHON_CMD -m venv venv
    echo -e "${GREEN}✅ Virtual environment created${NC}"
fi

# Activate virtual environment and install dependencies
echo "Installing Python dependencies..."
source venv/bin/activate

# Check if requirements.txt exists
if [ -f "requirements.txt" ]; then
    pip install -r requirements.txt
    echo -e "${GREEN}✅ Python dependencies installed${NC}"
else
    echo -e "${YELLOW}⚠️  requirements.txt not found. Skipping Python dependencies.${NC}"
fi

echo ""
echo -e "${YELLOW}⚛️  Setting up React frontend...${NC}"

# Install frontend dependencies
if [ -d "frontend" ]; then
    cd frontend
    
    if [ -f "package.json" ]; then
        echo "Installing Node.js dependencies (this may take a few minutes)..."
        npm install
        echo -e "${GREEN}✅ Frontend dependencies installed${NC}"
    else
        echo -e "${YELLOW}⚠️  package.json not found in frontend directory${NC}"
    fi
    
    cd ..
else
    echo -e "${YELLOW}⚠️  Frontend directory not found${NC}"
fi

echo ""
echo -e "${YELLOW}📝 Setting up environment configuration...${NC}"

# Create .env file if it doesn't exist
if [ -f ".env.example" ]; then
    if [ ! -f ".env" ]; then
        cp .env.example .env
        echo -e "${GREEN}✅ Created .env file from .env.example${NC}"
    else
        echo -e "${YELLOW}⚠️  .env file already exists. Skipping.${NC}"
    fi
else
    echo -e "${YELLOW}⚠️  .env.example not found. You may need to configure environment variables manually.${NC}"
fi

echo ""
echo -e "${GREEN}✨ Setup Complete!${NC}"
echo -e "${GREEN}==================${NC}"
echo ""
echo -e "${CYAN}🚀 To start the application:${NC}"
echo ""
echo -e "${NC}1. Start the backend API:${NC}"
echo -e "   ${YELLOW}source venv/bin/activate${NC}"
echo -e "   ${YELLOW}uvicorn api.main:app --reload${NC}"
echo ""
echo -e "${NC}2. Start the frontend (in a new terminal):${NC}"
echo -e "   ${YELLOW}cd frontend${NC}"
echo -e "   ${YELLOW}npm run dev${NC}"
echo ""
echo -e "${NC}3. Open your browser:${NC}"
echo -e "   ${YELLOW}Frontend: http://localhost:5173${NC}"
echo -e "   ${YELLOW}API Docs: http://localhost:8000/api/docs${NC}"
echo ""
echo -e "${CYAN}💡 Demo Mode Features:${NC}"
echo -e "   • Dark theme UI with responsive design"
echo -e "   • 5 AI consultant agents"
echo -e "   • Real-time confidence tracking"
echo -e "   • AWS architecture visualization"
echo -e "   • Code preview with syntax highlighting"
echo ""
echo -e "${CYAN}📚 For more information, see SETUP.md${NC}"
echo ""
