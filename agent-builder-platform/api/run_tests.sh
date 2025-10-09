#!/bin/bash
# Test Runner Script for Linux/Mac
# Runs comprehensive API tests using the virtual environment

echo "================================================================================"
echo "Agent Builder Platform - API Test Suite"
echo "================================================================================"
echo ""

# Check if venv exists
if [ ! -f "../../venv/bin/activate" ]; then
    echo "Error: Virtual environment not found at ../../venv"
    echo "Please create a virtual environment first:"
    echo "  python3 -m venv venv"
    echo "  source venv/bin/activate"
    echo "  pip install -r requirements.txt"
    exit 1
fi

# Activate virtual environment
echo "Activating virtual environment..."
source ../../venv/bin/activate

# Check if FastAPI is installed
python -c "import fastapi" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "Error: FastAPI not installed in virtual environment"
    echo "Installing dependencies..."
    pip install fastapi uvicorn pydantic pytest httpx
fi

echo ""
echo "================================================================================"
echo "Running Comprehensive API Tests"
echo "================================================================================"
echo ""

# Run the comprehensive test runner
python run_all_tests.py

# Capture exit code
TEST_EXIT_CODE=$?

echo ""
echo "================================================================================"
echo "Test Execution Complete"
echo "================================================================================"
echo ""

if [ $TEST_EXIT_CODE -eq 0 ]; then
    echo "Result: ALL TESTS PASSED"
else
    echo "Result: SOME TESTS FAILED"
fi

# Deactivate virtual environment
deactivate

exit $TEST_EXIT_CODE
