# Agent Builder Platform - Windows Setup Script
# This script automates the setup process for Windows

Write-Host "Agent Builder Platform - Automated Setup" -ForegroundColor Cyan
Write-Host "=========================================" -ForegroundColor Cyan
Write-Host ""

$setupErrors = 0

# Check Python installation
Write-Host "Checking prerequisites..." -ForegroundColor Yellow
try {
    $pythonVersion = python --version 2>&1
    Write-Host "[OK] Python found: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "[ERROR] Python not found. Please install Python 3.9+ from https://www.python.org/" -ForegroundColor Red
    $setupErrors++
}

# Check Node.js installation
try {
    $nodeVersion = node --version 2>&1
    Write-Host "[OK] Node.js found: $nodeVersion" -ForegroundColor Green
} catch {
    Write-Host "[ERROR] Node.js not found. Please install Node.js 18+ from https://nodejs.org/" -ForegroundColor Red
    $setupErrors++
}

# Check npm installation
try {
    $npmVersion = npm --version 2>&1
    Write-Host "[OK] npm found: v$npmVersion" -ForegroundColor Green
} catch {
    Write-Host "[ERROR] npm not found. Please install Node.js 18+ (includes npm) from https://nodejs.org/" -ForegroundColor Red
    $setupErrors++
}

# Exit if prerequisites are missing
if ($setupErrors -gt 0) {
    Write-Host ""
    Write-Host "[ERROR] Setup cannot continue. Please install missing prerequisites." -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "Setting up Python backend..." -ForegroundColor Yellow

# Create virtual environment
if (Test-Path "venv") {
    Write-Host "[WARNING] Virtual environment already exists. Skipping creation." -ForegroundColor Yellow
} else {
    Write-Host "Creating Python virtual environment..."
    python -m venv venv
    Write-Host "[OK] Virtual environment created" -ForegroundColor Green
}

# Activate virtual environment and install dependencies
Write-Host "Installing Python dependencies..."
& .\venv\Scripts\Activate.ps1

# Check if requirements.txt exists
if (Test-Path "requirements.txt") {
    pip install -r requirements.txt
    Write-Host "[OK] Python dependencies installed" -ForegroundColor Green
} else {
    Write-Host "[WARNING] requirements.txt not found. Skipping Python dependencies." -ForegroundColor Yellow
}

Write-Host ""
Write-Host "Setting up React frontend..." -ForegroundColor Yellow

# Install frontend dependencies
if (Test-Path "frontend") {
    Set-Location frontend
    
    if (Test-Path "package.json") {
        Write-Host "Installing Node.js dependencies (this may take a few minutes)..."
        npm install
        Write-Host "[OK] Frontend dependencies installed" -ForegroundColor Green
    } else {
        Write-Host "[WARNING] package.json not found in frontend directory" -ForegroundColor Yellow
    }
    
    Set-Location ..
} else {
    Write-Host "[WARNING] Frontend directory not found" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "Setting up environment configuration..." -ForegroundColor Yellow

# Create .env file if it doesn't exist
if (Test-Path ".env.example") {
    if (-not (Test-Path ".env")) {
        Copy-Item ".env.example" ".env"
        Write-Host "[OK] Created .env file from .env.example" -ForegroundColor Green
    } else {
        Write-Host "[WARNING] .env file already exists. Skipping." -ForegroundColor Yellow
    }
} else {
    Write-Host "[WARNING] .env.example not found. You may need to configure environment variables manually." -ForegroundColor Yellow
}

Write-Host ""
Write-Host "Setup Complete!" -ForegroundColor Green
Write-Host "===============" -ForegroundColor Green
Write-Host ""
Write-Host "To start the application:" -ForegroundColor Cyan
Write-Host ""
Write-Host "1. Start the backend API:" -ForegroundColor White
Write-Host "   .\venv\Scripts\Activate.ps1" -ForegroundColor Gray
Write-Host "   uvicorn api.main:app --reload" -ForegroundColor Gray
Write-Host ""
Write-Host "2. Start the frontend (in a new terminal):" -ForegroundColor White
Write-Host "   cd frontend" -ForegroundColor Gray
Write-Host "   npm run dev" -ForegroundColor Gray
Write-Host ""
Write-Host "3. Open your browser:" -ForegroundColor White
Write-Host "   Frontend: http://localhost:5173" -ForegroundColor Gray
Write-Host "   API Docs: http://localhost:8000/api/docs" -ForegroundColor Gray
Write-Host ""
Write-Host "Demo Mode Features:" -ForegroundColor Cyan
Write-Host "   - Dark theme UI with responsive design" -ForegroundColor Gray
Write-Host "   - 5 AI consultant agents" -ForegroundColor Gray
Write-Host "   - Real-time confidence tracking" -ForegroundColor Gray
Write-Host "   - AWS architecture visualization" -ForegroundColor Gray
Write-Host "   - Code preview with syntax highlighting" -ForegroundColor Gray
Write-Host ""
Write-Host "To run tests:" -ForegroundColor Cyan
Write-Host "   .\run_comprehensive_tests.bat" -ForegroundColor Gray
Write-Host ""
Write-Host "For more information, see SETUP.md" -ForegroundColor Cyan
Write-Host ""
