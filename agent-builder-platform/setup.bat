@echo off
REM Agent Builder Platform - Windows CMD Setup Script
REM This script automates the setup process for Windows Command Prompt

echo Agent Builder Platform - Automated Setup
echo =========================================
echo.

set SETUP_ERRORS=0

REM Check Python installation
echo Checking prerequisites...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Python not found. Please install Python 3.9+ from https://www.python.org/
    set /a SETUP_ERRORS+=1
) else (
    for /f "tokens=*" %%i in ('python --version') do echo [OK] Python found: %%i
)

REM Check Node.js installation
node --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Node.js not found. Please install Node.js 18+ from https://nodejs.org/
    set /a SETUP_ERRORS+=1
) else (
    for /f "tokens=*" %%i in ('node --version') do echo [OK] Node.js found: %%i
)

REM Check npm installation
npm --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] npm not found. Please install Node.js 18+ (includes npm) from https://nodejs.org/
    set /a SETUP_ERRORS+=1
) else (
    for /f "tokens=*" %%i in ('npm --version') do echo [OK] npm found: v%%i
)

REM Exit if prerequisites are missing
if %SETUP_ERRORS% gtr 0 (
    echo.
    echo [ERROR] Setup cannot continue. Please install missing prerequisites.
    exit /b 1
)

echo.
echo Setting up Python backend...

REM Create virtual environment
if exist venv (
    echo [WARNING] Virtual environment already exists. Skipping creation.
) else (
    echo Creating Python virtual environment...
    python -m venv venv
    if %errorlevel% equ 0 (
        echo [OK] Virtual environment created
    ) else (
        echo [ERROR] Failed to create virtual environment
        exit /b 1
    )
)

REM Activate virtual environment and install dependencies
echo Installing Python dependencies...
call venv\Scripts\activate.bat

REM Check if requirements.txt exists
if exist requirements.txt (
    pip install -r requirements.txt
    if %errorlevel% equ 0 (
        echo [OK] Python dependencies installed
    ) else (
        echo [ERROR] Failed to install Python dependencies
        exit /b 1
    )
) else (
    echo [WARNING] requirements.txt not found. Skipping Python dependencies.
)

echo.
echo Setting up React frontend...

REM Install frontend dependencies
if exist frontend (
    cd frontend
    
    if exist package.json (
        echo Installing Node.js dependencies (this may take a few minutes)...
        call npm install
        if %errorlevel% equ 0 (
            echo [OK] Frontend dependencies installed
        ) else (
            echo [ERROR] Failed to install frontend dependencies
            cd ..
            exit /b 1
        )
    ) else (
        echo [WARNING] package.json not found in frontend directory
    )
    
    cd ..
) else (
    echo [WARNING] Frontend directory not found
)

echo.
echo Setting up environment configuration...

REM Create .env file if it doesn't exist
if exist .env.example (
    if not exist .env (
        copy .env.example .env >nul
        echo [OK] Created .env file from .env.example
    ) else (
        echo [WARNING] .env file already exists. Skipping.
    )
) else (
    echo [WARNING] .env.example not found. You may need to configure environment variables manually.
)

echo.
echo Setup Complete!
echo ===============
echo.
echo To start the application:
echo.
echo 1. Start the backend API:
echo    venv\Scripts\activate.bat
echo    uvicorn api.main:app --reload
echo.
echo 2. Start the frontend (in a new CMD window):
echo    cd frontend
echo    npm run dev
echo.
echo 3. Open your browser:
echo    Frontend: http://localhost:5173
echo    API Docs: http://localhost:8000/api/docs
echo.
echo Demo Mode Features:
echo    - Dark theme UI with responsive design
echo    - 5 AI consultant agents
echo    - Real-time confidence tracking
echo    - AWS architecture visualization
echo    - Code preview with syntax highlighting
echo.
echo To run tests:
echo    run_comprehensive_tests.bat
echo.
echo For more information, see SETUP.md
echo.
