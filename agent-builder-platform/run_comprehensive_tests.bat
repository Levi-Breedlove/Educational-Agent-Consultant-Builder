@echo off
REM Comprehensive Test Suite for Agent Builder Platform (Windows)
REM Runs all API tests and validation checks

echo ================================================================================
echo AGENT BUILDER PLATFORM - COMPREHENSIVE TEST SUITE
echo ================================================================================
echo.

REM Check if virtual environment exists
if not exist "venv" (
    echo [ERROR] Virtual environment not found!
    echo Please run setup.bat first to create the virtual environment.
    echo.
    pause
    exit /b 1
)

REM Activate the virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat

if errorlevel 1 (
    echo [ERROR] Failed to activate virtual environment
    echo Please ensure venv exists and is properly configured
    echo.
    pause
    exit /b 1
)

echo [OK] Virtual environment activated
echo.

REM Navigate to API directory
cd api

echo ================================================================================
echo Running API Test Suite
echo ================================================================================
echo.

REM Run all API tests
echo Running all API tests...
python run_all_tests.py

REM Capture exit code
set TEST_EXIT_CODE=%errorlevel%

echo.
echo ================================================================================
echo Test Results
echo ================================================================================
echo.

if %TEST_EXIT_CODE% equ 0 (
    echo [OK] All tests passed successfully!
) else (
    echo [ERROR] Some tests failed. Exit code: %TEST_EXIT_CODE%
)

echo.
echo ================================================================================
echo Test execution completed
echo ================================================================================
echo.

REM Return to parent directory
cd ..

REM Deactivate virtual environment
call venv\Scripts\deactivate.bat

REM Pause to see results
pause

exit /b %TEST_EXIT_CODE%
