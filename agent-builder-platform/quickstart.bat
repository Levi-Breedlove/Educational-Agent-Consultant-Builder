@echo off
REM Agent Builder Platform - Quick Start Script
REM This script does EVERYTHING: setup + start servers automatically

echo ========================================
echo Agent Builder Platform - Quick Start
echo ========================================
echo.
echo This script will:
echo 1. Check prerequisites
echo 2. Install all dependencies
echo 3. Start backend and frontend servers
echo.
pause

set SETUP_ERRORS=0

REM Detect Python command
py --version >nul 2>&1
if %errorlevel% neq 0 (
    python --version >nul 2>&1
    if %errorlevel% neq 0 (
        echo [ERROR] Python not found. Please install Python 3.9+ from https://www.python.org/
        set /a SETUP_ERRORS+=1
    ) else (
        for /f "tokens=*" %%i in ('python --version') do echo [OK] Python found: %%i
        set PYTHON_CMD=python
    )
) else (
    for /f "tokens=*" %%i in ('py --version') do echo [OK] Python found: %%i
    set PYTHON_CMD=py
)

REM Check Node.js
node --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Node.js not found. Please install Node.js 18+ from https://nodejs.org/
    set /a SETUP_ERRORS+=1
) else (
    for /f "tokens=*" %%i in ('node --version') do echo [OK] Node.js found: %%i
)

REM Check npm
npm --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] npm not found. Please install Node.js 18+ from https://nodejs.org/
    set /a SETUP_ERRORS+=1
) else (
    for /f "tokens=*" %%i in ('npm --version') do echo [OK] npm found: v%%i
)

if %SETUP_ERRORS% gtr 0 (
    echo.
    echo [ERROR] Missing prerequisites. Please install them and try again.
    pause
    exit /b 1
)

echo.
echo ========================================
echo Step 1: Setting up Python backend...
echo ========================================
echo.

REM Create venv at root level
cd ..
if exist venv (
    echo [OK] Virtual environment already exists
) else (
    echo Creating Python virtual environment...
    %PYTHON_CMD% -m venv venv
    if %errorlevel% equ 0 (
        echo [OK] Virtual environment created
    ) else (
        echo [ERROR] Failed to create virtual environment
        cd agent-builder-platform
        pause
        exit /b 1
    )
)

REM Activate venv and install Python dependencies
echo Installing Python dependencies...
call venv\Scripts\activate.bat
cd agent-builder-platform

if exist requirements.txt (
    pip install -r requirements.txt
    if %errorlevel% equ 0 (
        echo [OK] Python dependencies installed
    ) else (
        echo [ERROR] Failed to install Python dependencies
        pause
        exit /b 1
    )
)

echo.
echo ========================================
echo Step 2: Setting up React frontend...
echo ========================================
echo.

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
            pause
            exit /b 1
        )
    )
    cd ..
)

REM Create .env file
if exist .env.example (
    if not exist .env (
        copy .env.example .env >nul
        echo [OK] Created .env file
    )
)

echo.
echo ========================================
echo Step 3: Starting servers...
echo ========================================
echo.

REM Get the absolute path to Hackathon-Preview directory
cd ..
set ROOT_DIR=%CD%
cd agent-builder-platform

REM Start backend in new window
echo Starting backend server...
start "Agent Builder - Backend" cmd /k "cd /d %ROOT_DIR% && venv\Scripts\activate.bat && cd agent-builder-platform && uvicorn api.main:app --reload"

REM Wait for backend to initialize
echo Waiting for backend to start...
timeout /t 5 /nobreak >nul

REM Start frontend in new window
echo Starting frontend server...
start "Agent Builder - Frontend" cmd /k "cd /d %ROOT_DIR%\agent-builder-platform\frontend && npm run dev"

echo.
echo ========================================
echo SUCCESS! Servers are starting...
echo ========================================
echo.
echo Backend:  http://localhost:8000/api/docs
echo Frontend: http://localhost:5173
echo.
echo Two new windows have opened:
echo - "Agent Builder - Backend" (backend server)
echo - "Agent Builder - Frontend" (frontend server)
echo.
echo To stop the servers, close those windows or press Ctrl+C in each.
echo.
echo Opening frontend in your browser in 5 seconds...
timeout /t 5 /nobreak >nul
start http://localhost:5173
echo.
echo Press any key to close this window (servers will keep running)...
pause >nul
