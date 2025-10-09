@echo off
REM Test Runner Script for Windows
REM Runs comprehensive API tests using the virtual environment

echo ================================================================================
echo Agent Builder Platform - API Test Suite
echo ================================================================================
echo.

REM Check if venv exists
if not exist "..\..\venv\Scripts\activate.bat" (
    echo Error: Virtual environment not found at ..\..\venv
    echo Please create a virtual environment first:
    echo   python -m venv venv
    echo   venv\Scripts\activate
    echo   pip install -r requirements.txt
    exit /b 1
)

REM Activate virtual environment
echo Activating virtual environment...
call ..\..\venv\Scripts\activate.bat

REM Check if FastAPI is installed
python -c "import fastapi" 2>nul
if errorlevel 1 (
    echo Error: FastAPI not installed in virtual environment
    echo Installing dependencies...
    pip install fastapi uvicorn pydantic pytest httpx
)

echo.
echo ================================================================================
echo Running Comprehensive API Tests
echo ================================================================================
echo.

REM Run the comprehensive test runner
python run_all_tests.py

REM Capture exit code
set TEST_EXIT_CODE=%ERRORLEVEL%

echo.
echo ================================================================================
echo Test Execution Complete
echo ================================================================================
echo.

if %TEST_EXIT_CODE% equ 0 (
    echo Result: ALL TESTS PASSED
) else (
    echo Result: SOME TESTS FAILED
)

REM Deactivate virtual environment
deactivate

exit /b %TEST_EXIT_CODE%
