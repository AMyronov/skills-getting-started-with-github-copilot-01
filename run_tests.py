#!/usr/bin/env python3
"""
Test runner script for the FastAPI application.
This script provides convenient ways to run different test categories.
"""

import subprocess
import sys
import os

def run_command(cmd, description):
    """Run a command and print its description."""
    print(f"\n{'='*60}")
    print(f"Running: {description}")
    print(f"Command: {cmd}")
    print('='*60)
    
    result = subprocess.run(cmd, shell=True, cwd="/workspaces/skills-getting-started-with-github-copilot-01")
    return result.returncode == 0

def main():
    """Main test runner function."""
    python_cmd = "/workspaces/skills-getting-started-with-github-copilot-01/.venv/bin/python"
    
    if len(sys.argv) > 1:
        test_type = sys.argv[1].lower()
    else:
        test_type = "all"
    
    success = True
    
    if test_type == "all" or test_type == "basic":
        # Run all tests
        success &= run_command(
            f"{python_cmd} -m pytest tests/ -v",
            "All Tests"
        )
    
    if test_type == "all" or test_type == "coverage":
        # Run tests with coverage
        success &= run_command(
            f"{python_cmd} -m pytest tests/ --cov=src --cov-report=term-missing",
            "Tests with Coverage Report"
        )
    
    if test_type == "endpoints":
        # Run only endpoint tests
        success &= run_command(
            f"{python_cmd} -m pytest tests/test_api.py::TestBasicEndpoints -v",
            "Basic Endpoint Tests"
        )
    
    if test_type == "signup":
        # Run only signup tests
        success &= run_command(
            f"{python_cmd} -m pytest tests/test_api.py::TestSignupEndpoint -v",
            "Signup Functionality Tests"
        )
    
    if test_type == "remove":
        # Run only remove participant tests
        success &= run_command(
            f"{python_cmd} -m pytest tests/test_api.py::TestRemoveParticipantEndpoint -v",
            "Remove Participant Tests"
        )
    
    if test_type == "edge":
        # Run only edge case tests
        success &= run_command(
            f"{python_cmd} -m pytest tests/test_api.py::TestEdgeCases -v",
            "Edge Case Tests"
        )
    
    if test_type == "help":
        print("""
Usage: python run_tests.py [test_type]

Available test types:
- all (default): Run all tests and coverage
- basic: Run all tests without coverage
- coverage: Run tests with coverage report only
- endpoints: Run basic endpoint tests
- signup: Run signup functionality tests
- remove: Run remove participant tests  
- edge: Run edge case tests
- help: Show this help message

Examples:
  python run_tests.py
  python run_tests.py coverage
  python run_tests.py signup
        """)
        return
    
    if success:
        print("\n🎉 All requested tests passed!")
        sys.exit(0)
    else:
        print("\n❌ Some tests failed!")
        sys.exit(1)

if __name__ == "__main__":
    main()