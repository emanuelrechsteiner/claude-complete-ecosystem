#!/usr/bin/env python3
"""
Comprehensive test runner for MCP Vector Server Agent Observation System.

This script provides automated testing capabilities with detailed reporting,
performance benchmarking, and coverage analysis.
"""

import sys
import subprocess
import argparse
import time
from pathlib import Path
from typing import List, Dict, Any


def run_command(command: List[str], description: str = None) -> Dict[str, Any]:
    """Run a command and return the result."""
    if description:
        print(f"\n🔧 {description}")
    
    print(f"   Running: {' '.join(command)}")
    
    start_time = time.time()
    try:
        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            check=False
        )
        end_time = time.time()
        
        return {
            "success": result.returncode == 0,
            "returncode": result.returncode,
            "stdout": result.stdout,
            "stderr": result.stderr,
            "duration": end_time - start_time,
            "command": " ".join(command)
        }
    except Exception as e:
        end_time = time.time()
        return {
            "success": False,
            "returncode": -1,
            "stdout": "",
            "stderr": str(e),
            "duration": end_time - start_time,
            "command": " ".join(command)
        }


def print_test_results(result: Dict[str, Any], test_name: str):
    """Print formatted test results."""
    status = "✅ PASS" if result["success"] else "❌ FAIL"
    duration = f"{result['duration']:.2f}s"
    
    print(f"\n{status} {test_name} ({duration})")
    
    if result["stdout"]:
        # Filter and show relevant output
        lines = result["stdout"].split('\n')
        summary_lines = [line for line in lines if any(keyword in line.lower() for keyword in [
            'passed', 'failed', 'error', 'warning', 'collected', '==', 'coverage'
        ])]
        
        if summary_lines:
            print("   Output:")
            for line in summary_lines[-10:]:  # Show last 10 relevant lines
                if line.strip():
                    print(f"     {line}")
    
    if result["stderr"] and not result["success"]:
        print("   Errors:")
        error_lines = result["stderr"].split('\n')
        for line in error_lines[-5:]:  # Show last 5 error lines
            if line.strip():
                print(f"     {line}")


def run_unit_tests(verbose: bool = False) -> Dict[str, Any]:
    """Run unit tests for models and individual components."""
    command = ["python", "-m", "pytest", "tests/test_models.py"]
    if verbose:
        command.append("-v")
    command.extend(["--tb=short", "-x"])  # Stop on first failure
    
    return run_command(command, "Running Unit Tests (Models)")


def run_mcp_tool_tests(verbose: bool = False) -> Dict[str, Any]:
    """Run MCP tool functionality tests."""
    command = ["python", "-m", "pytest", "tests/test_mcp_tools.py"]
    if verbose:
        command.append("-v")
    command.extend(["--tb=short", "-x"])
    
    return run_command(command, "Running MCP Tool Tests")


def run_integration_tests(verbose: bool = False) -> Dict[str, Any]:
    """Run integration tests."""
    command = ["python", "-m", "pytest", "tests/test_integration.py"]
    if verbose:
        command.append("-v")
    command.extend(["--tb=short"])
    
    return run_command(command, "Running Integration Tests")


def run_performance_tests(verbose: bool = False) -> Dict[str, Any]:
    """Run performance benchmarking tests."""
    command = ["python", "-m", "pytest", "tests/test_performance.py"]
    if verbose:
        command.extend(["-v", "-s"])  # Show print statements for benchmarks
    command.extend(["--tb=short"])
    
    return run_command(command, "Running Performance Tests")


def run_all_tests(verbose: bool = False) -> Dict[str, Any]:
    """Run all tests together."""
    command = ["python", "-m", "pytest", "tests/"]
    if verbose:
        command.append("-v")
    command.extend(["--tb=short"])
    
    return run_command(command, "Running All Tests")


def run_coverage_analysis() -> Dict[str, Any]:
    """Run tests with coverage analysis."""
    command = [
        "python", "-m", "pytest", "tests/",
        "--cov=mcp_vector_server",
        "--cov-report=term-missing",
        "--cov-report=html:htmlcov",
        "--cov-fail-under=80",
        "--tb=short"
    ]
    
    return run_command(command, "Running Coverage Analysis")


def run_specific_test(test_path: str, verbose: bool = False) -> Dict[str, Any]:
    """Run a specific test file or test function."""
    command = ["python", "-m", "pytest", test_path]
    if verbose:
        command.append("-v")
    command.extend(["--tb=short", "-s"])
    
    return run_command(command, f"Running Specific Test: {test_path}")


def install_test_dependencies() -> Dict[str, Any]:
    """Install required test dependencies."""
    dependencies = [
        "pytest>=7.0.0",
        "pytest-cov>=4.0.0", 
        "psutil>=5.8.0",
        "pydantic>=2.0.0"
    ]
    
    command = ["pip", "install"] + dependencies
    return run_command(command, "Installing Test Dependencies")


def check_test_environment() -> bool:
    """Check if test environment is properly set up."""
    print("🔍 Checking Test Environment")
    
    # Check Python version
    if sys.version_info < (3, 8):
        print("❌ Python 3.8+ required")
        return False
    
    print(f"✅ Python {sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}")
    
    # Check if in correct directory
    if not Path("tests").exists():
        print("❌ Tests directory not found. Run from project root.")
        return False
    
    print("✅ Tests directory found")
    
    # Check if source module can be imported
    try:
        import mcp_vector_server
        print("✅ mcp_vector_server module can be imported")
    except ImportError as e:
        print(f"❌ Cannot import mcp_vector_server: {e}")
        return False
    
    # Check pytest installation
    try:
        import pytest
        print(f"✅ pytest {pytest.__version__} available")
    except ImportError:
        print("❌ pytest not installed")
        return False
    
    return True


def generate_test_report(results: Dict[str, Dict[str, Any]]):
    """Generate a comprehensive test report."""
    print("\n" + "="*80)
    print("📊 TEST EXECUTION SUMMARY")
    print("="*80)
    
    total_duration = sum(result["duration"] for result in results.values())
    passed_tests = sum(1 for result in results.values() if result["success"])
    total_tests = len(results)
    
    print(f"Total Tests Run: {total_tests}")
    print(f"Passed: {passed_tests}")
    print(f"Failed: {total_tests - passed_tests}")
    print(f"Total Duration: {total_duration:.2f}s")
    print(f"Success Rate: {(passed_tests/total_tests)*100:.1f}%")
    
    print("\n📋 Detailed Results:")
    for test_name, result in results.items():
        status = "✅" if result["success"] else "❌"
        duration = f"{result['duration']:.2f}s"
        print(f"  {status} {test_name:<30} {duration}")
    
    if any(not result["success"] for result in results.values()):
        print("\n⚠️  Failed Tests:")
        for test_name, result in results.items():
            if not result["success"]:
                print(f"  ❌ {test_name}")
                if result["stderr"]:
                    error_summary = result["stderr"].split('\n')[0]
                    print(f"     Error: {error_summary}")


def main():
    """Main test runner function."""
    parser = argparse.ArgumentParser(description="MCP Vector Server Test Runner")
    parser.add_argument(
        "test_type",
        nargs="?",
        choices=["unit", "mcp", "integration", "performance", "all", "coverage", "install-deps"],
        default="all",
        help="Type of tests to run"
    )
    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Verbose output"
    )
    parser.add_argument(
        "--specific", "-s",
        type=str,
        help="Run specific test file or function (e.g., tests/test_models.py::TestObservationMetadata)"
    )
    parser.add_argument(
        "--no-env-check",
        action="store_true",
        help="Skip environment check"
    )
    
    args = parser.parse_args()
    
    # Check environment unless skipped
    if not args.no_env_check:
        if not check_test_environment():
            print("\n❌ Environment check failed. Use --no-env-check to skip.")
            sys.exit(1)
    
    results = {}
    
    try:
        if args.specific:
            # Run specific test
            result = run_specific_test(args.specific, args.verbose)
            print_test_results(result, f"Specific Test: {args.specific}")
            results[args.specific] = result
            
        elif args.test_type == "install-deps":
            # Install dependencies
            result = install_test_dependencies()
            print_test_results(result, "Dependency Installation")
            results["install-deps"] = result
            
        elif args.test_type == "unit":
            # Run unit tests only
            result = run_unit_tests(args.verbose)
            print_test_results(result, "Unit Tests")
            results["unit"] = result
            
        elif args.test_type == "mcp":
            # Run MCP tool tests only
            result = run_mcp_tool_tests(args.verbose)
            print_test_results(result, "MCP Tool Tests")
            results["mcp"] = result
            
        elif args.test_type == "integration":
            # Run integration tests only
            result = run_integration_tests(args.verbose)
            print_test_results(result, "Integration Tests")
            results["integration"] = result
            
        elif args.test_type == "performance":
            # Run performance tests only
            result = run_performance_tests(args.verbose)
            print_test_results(result, "Performance Tests")
            results["performance"] = result
            
        elif args.test_type == "coverage":
            # Run coverage analysis
            result = run_coverage_analysis()
            print_test_results(result, "Coverage Analysis")
            results["coverage"] = result
            
            if result["success"]:
                print(f"\n📈 Coverage report generated in htmlcov/index.html")
            
        elif args.test_type == "all":
            # Run all test suites sequentially
            test_suites = [
                ("Unit Tests", run_unit_tests),
                ("MCP Tool Tests", run_mcp_tool_tests),
                ("Integration Tests", run_integration_tests), 
                ("Performance Tests", run_performance_tests)
            ]
            
            for test_name, test_function in test_suites:
                result = test_function(args.verbose)
                print_test_results(result, test_name)
                results[test_name] = result
                
                # Stop on critical failures for unit and MCP tests
                if not result["success"] and test_name in ["Unit Tests", "MCP Tool Tests"]:
                    print(f"\n⚠️  Critical test failure in {test_name}. Stopping execution.")
                    break
    
    except KeyboardInterrupt:
        print("\n\n⏹️  Test execution interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Unexpected error during test execution: {e}")
        sys.exit(1)
    
    # Generate summary report
    if results:
        generate_test_report(results)
        
        # Exit with error code if any tests failed
        if any(not result["success"] for result in results.values()):
            print(f"\n❌ Some tests failed. Check output above for details.")
            sys.exit(1)
        else:
            print(f"\n✅ All tests passed successfully!")
            sys.exit(0)
    else:
        print(f"\n⚠️  No tests were executed.")
        sys.exit(1)


if __name__ == "__main__":
    main()