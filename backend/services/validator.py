"""
Code Validation Engine

Safely executes Python code with test cases and returns results.
Includes timeout protection and error handling.
"""

import sys
import io
import json
from typing import Dict, Any, List
from contextlib import redirect_stdout, redirect_stderr
import signal
from functools import wraps


class TimeoutError(Exception):
    """Custom exception for code execution timeout"""
    pass


def timeout_handler(signum, frame):
    """Handler for timeout signal"""
    raise TimeoutError("Code execution timed out")


def with_timeout(seconds: int):
    """Decorator to add timeout to function execution"""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Set the signal handler and alarm
            signal.signal(signal.SIGALRM, timeout_handler)
            signal.alarm(seconds)
            try:
                result = func(*args, **kwargs)
            finally:
                # Disable the alarm
                signal.alarm(0)
            return result
        return wrapper
    return decorator


def execute_code_safely(code: str, timeout_seconds: int = 3) -> Dict[str, Any]:
    """
    Execute Python code safely with timeout protection.
    
    Args:
        code: The Python code to execute
        timeout_seconds: Maximum execution time in seconds (default: 3)
    
    Returns:
        Dictionary containing execution results:
        {
            "success": bool,
            "output": str,
            "error": str or None,
            "timeout": bool
        }
    """
    # Create string buffers to capture output
    stdout_buffer = io.StringIO()
    stderr_buffer = io.StringIO()
    
    result = {
        "success": False,
        "output": "",
        "error": None,
        "timeout": False
    }
    
    try:
        # Create a restricted namespace for code execution
        namespace = {
            '__builtins__': {
                # Allow only safe built-in functions
                'print': print,
                'len': len,
                'range': range,
                'str': str,
                'int': int,
                'float': float,
                'bool': bool,
                'list': list,
                'dict': dict,
                'tuple': tuple,
                'set': set,
                'abs': abs,
                'max': max,
                'min': min,
                'sum': sum,
                'sorted': sorted,
                'enumerate': enumerate,
                'zip': zip,
                'map': map,
                'filter': filter,
                'all': all,
                'any': any,
                'isinstance': isinstance,
                'type': type,
            }
        }
        
        # Redirect stdout and stderr
        with redirect_stdout(stdout_buffer), redirect_stderr(stderr_buffer):
            # Set alarm for timeout (Unix-like systems only)
            if hasattr(signal, 'SIGALRM'):
                signal.signal(signal.SIGALRM, timeout_handler)
                signal.alarm(timeout_seconds)
            
            try:
                # Execute the code
                exec(code, namespace)
                result["success"] = True
                result["output"] = stdout_buffer.getvalue()
                
            except TimeoutError:
                result["timeout"] = True
                result["error"] = f"Code execution exceeded {timeout_seconds} seconds timeout"
                
            except Exception as e:
                result["error"] = f"{type(e).__name__}: {str(e)}"
                result["output"] = stdout_buffer.getvalue()
                
            finally:
                # Disable alarm
                if hasattr(signal, 'SIGALRM'):
                    signal.alarm(0)
    
    except Exception as e:
        result["error"] = f"Execution setup error: {str(e)}"
    
    # Capture any stderr output
    stderr_output = stderr_buffer.getvalue()
    if stderr_output:
        result["error"] = (result["error"] or "") + "\n" + stderr_output
    
    return result


def validate_submission(code: str, test_cases: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Validate student code against test cases.
    
    Args:
        code: The student's submitted code
        test_cases: List of test case dictionaries with format:
            {
                "input": "input data",
                "expected_output": "expected result",
                "description": "what this test checks"
            }
    
    Returns:
        Dictionary containing validation results:
        {
            "passed": int,
            "failed": int,
            "total": int,
            "test_results": [
                {
                    "test_number": int,
                    "description": str,
                    "passed": bool,
                    "expected": str,
                    "actual": str,
                    "error": str or None
                }
            ],
            "overall_status": "passed" | "failed" | "error"
        }
    """
    results = {
        "passed": 0,
        "failed": 0,
        "total": len(test_cases),
        "test_results": [],
        "overall_status": "failed"
    }
    
    for i, test_case in enumerate(test_cases, 1):
        test_result = {
            "test_number": i,
            "description": test_case.get("description", f"Test case {i}"),
            "passed": False,
            "expected": test_case.get("expected_output", ""),
            "actual": "",
            "error": None
        }
        
        # Prepare code with test input
        test_input = test_case.get("input", "")
        test_code = f"{code}\n\n# Test input\n{test_input}"
        
        # Execute the code
        execution_result = execute_code_safely(test_code, timeout_seconds=3)
        
        if execution_result["timeout"]:
            test_result["error"] = "Timeout"
            test_result["actual"] = "Code execution timed out"
            
        elif execution_result["error"]:
            test_result["error"] = execution_result["error"]
            test_result["actual"] = execution_result["output"] or "No output"
            
        else:
            # Compare output with expected
            actual_output = execution_result["output"].strip()
            expected_output = str(test_case.get("expected_output", "")).strip()
            
            test_result["actual"] = actual_output
            
            if actual_output == expected_output:
                test_result["passed"] = True
                results["passed"] += 1
            else:
                results["failed"] += 1
        
        results["test_results"].append(test_result)
    
    # Determine overall status
    if results["passed"] == results["total"]:
        results["overall_status"] = "passed"
    elif results["passed"] > 0:
        results["overall_status"] = "partial"
    else:
        results["overall_status"] = "failed"
    
    return results


def check_code_safety(code: str) -> Dict[str, Any]:
    """
    Check if code contains potentially dangerous operations.
    
    Args:
        code: The code to check
    
    Returns:
        Dictionary with safety check results:
        {
            "safe": bool,
            "warnings": List[str],
            "blocked_operations": List[str]
        }
    """
    dangerous_keywords = [
        'import os', 'import sys', 'import subprocess',
        'import socket', 'import requests', 'import urllib',
        '__import__', 'eval', 'exec', 'compile',
        'open(', 'file(', 'input(',
        'os.', 'sys.', 'subprocess.',
    ]
    
    warnings = []
    blocked_operations = []
    
    code_lower = code.lower()
    
    for keyword in dangerous_keywords:
        if keyword.lower() in code_lower:
            blocked_operations.append(keyword)
            warnings.append(f"Potentially dangerous operation detected: {keyword}")
    
    return {
        "safe": len(blocked_operations) == 0,
        "warnings": warnings,
        "blocked_operations": blocked_operations
    }


# Made with Bob