#!/usr/bin/env python3
"""
Comprehensive Test Runner
Runs all API tests including comprehensive tests, performance benchmarks, and integration tests
"""

import sys
import os
import subprocess
import time
from datetime import datetime

# Test files to run
TEST_FILES = [
    "test_api_comprehensive.py",
    "test_performance_benchmarks.py",
    "test_integration_orchestrator.py",
    "test_session_management.py",
    "test_workflow_endpoints.py",
    "test_testing_endpoints.py",
    "test_export_endpoints.py",
    "test_performance_service.py"
]

def print_header(title):
    """Print formatted header"""
    print()
    print("=" * 80)
    print(title.center(80))
    print("=" * 80)
    print()

def print_section(title):
    """Print formatted section"""
    print()
    print("-" * 80)
    print(title)
    print("-" * 80)

def run_test_file(test_file):
    """Run a single test file"""
    print(f"\nRunning {test_file}...")
    print("-" * 80)
    
    start_time = time.time()
    
    try:
        # Run the test file
        result = subprocess.run(
            [sys.executable, test_file],
            cwd=os.path.dirname(__file__),
            capture_output=True,
            text=True,
            timeout=300  # 5 minute timeout
        )
        
        duration = time.time() - start_time
        
        # Print output
        if result.stdout:
            print(result.stdout)
        
        if result.stderr:
            print("STDERR:", result.stderr)
        
        # Check result
        if result.returncode == 0:
            print(f"[PASS] {test_file} ({duration:.2f}s)")
            return True, duration
        else:
            print(f"[FAIL] {test_file} ({duration:.2f}s)")
            return False, duration
            
    except subprocess.TimeoutExpired:
        print(f"[TIMEOUT] {test_file} (exceeded 5 minutes)")
        return False, 300
    except Exception as e:
        print(f"[ERROR] {test_file}: {e}")
        return False, 0

def main():
    """Main test runner"""
    print_header("AGENT BUILDER PLATFORM - COMPREHENSIVE TEST SUITE")
    
    print(f"Start Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Python Version: {sys.version}")
    print(f"Working Directory: {os.getcwd()}")
    print()
    
    # Check if test files exist
    print_section("Checking Test Files")
    missing_files = []
    for test_file in TEST_FILES:
        file_path = os.path.join(os.path.dirname(__file__), test_file)
        if os.path.exists(file_path):
            print(f"  [OK] {test_file}")
        else:
            print(f"  [MISSING] {test_file} (not found)")
            missing_files.append(test_file)
    
    if missing_files:
        print(f"\nWarning: {len(missing_files)} test file(s) not found")
        print("Continuing with available tests...")
    
    # Run tests
    print_section("Running Tests")
    
    results = {}
    total_duration = 0
    
    for test_file in TEST_FILES:
        file_path = os.path.join(os.path.dirname(__file__), test_file)
        if os.path.exists(file_path):
            passed, duration = run_test_file(test_file)
            results[test_file] = passed
            total_duration += duration
        else:
            results[test_file] = None  # Skip missing files
    
    # Summary
    print_header("TEST SUMMARY")
    
    passed_count = sum(1 for v in results.values() if v is True)
    failed_count = sum(1 for v in results.values() if v is False)
    skipped_count = sum(1 for v in results.values() if v is None)
    total_count = len(results)
    
    print(f"Total Tests: {total_count}")
    print(f"Passed: {passed_count}")
    print(f"Failed: {failed_count}")
    print(f"Skipped: {skipped_count}")
    print(f"Total Duration: {total_duration:.2f}s")
    print()
    
    # Detailed results
    print("Detailed Results:")
    print("-" * 80)
    for test_file, result in results.items():
        if result is True:
            status = "[PASS]"
        elif result is False:
            status = "[FAIL]"
        else:
            status = "[SKIP]"
        print(f"  {status:12} {test_file}")
    
    print()
    print(f"End Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Exit code
    if failed_count > 0:
        print()
        print("=" * 80)
        print("SOME TESTS FAILED".center(80))
        print("=" * 80)
        return 1
    elif passed_count == 0:
        print()
        print("=" * 80)
        print("NO TESTS RAN".center(80))
        print("=" * 80)
        return 1
    else:
        print()
        print("=" * 80)
        print("ALL TESTS PASSED".center(80))
        print("=" * 80)
        return 0

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
