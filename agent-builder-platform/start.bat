@echo off
REM Agent Builder Platform - Start Script
REM This script starts both backend and frontend in separate windows

echo Starting Agent Builder Platform...
echo.

REM Check if venv exists
if not exist ..\venv (
    echo [ERROR] Virtual environment not found!
    echo Please run setup.bat first to set up the project.
    pause
    exit /b 1
)

REM Start backend in a new window
echo Starting backend server...
start "Agent Builder - Backend" cmd /k "cd /d %~dp0.. && venv\Scripts\activate.bat && cd agent-builder-platform && uvicorn api.main:app --reload"

REM Wait a moment for backend to start
timeout /t 3 /nobreak >nul

REM Start frontend in a new window
echo Starting frontend server...
start "Agent Builder - Frontend" cmd /k "cd /d %~dp0frontend && npm run dev"

echo.
echo [OK] Both servers are starting in separate windows!
echo.
echo Backend: http://localhost:8000/api/docs
echo Frontend: http://localhost:5173
echo.
echo Press any key to exit this window (servers will keep running)...
pause >nul
