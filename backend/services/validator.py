"""
Code Validation Engine

Safely executes Python code with test cases and returns results.
Includes cross-platform timeout protection, AST-based security validation,
and proper resource management.
"""

import sys
import io
import json
import ast
import multiprocessing
from typing import Dict, Any, List, Optional, Set
from contextlib import redirect_stdout, redirect_stderr
from functools import wraps

from config import (
    CODE_EXECUTION_TIMEOUT,
    MAX_CODE_LENGTH,
    MAX_TEST_CASES,
    FORBIDDEN_IMPORTS,
    FORBIDDEN_BUILTINS
)


class TimeoutError(Exception):
    """Custom exception for code execution timeout"""
    pass


class SecurityError(Exception):
    """Custom exception for security violations"""
    pass


class ASTSecurityValidator(ast.NodeVisitor):
    """
    AST-based security validator that checks for dangerous operations.
    This cannot be bypassed with string concatenation or other tricks.
    """
    
    def __init__(self):
        self.violations: List[str] = []
        self.imported_modules: Set[str] = set()
    
    def visit_Import(self, node: ast.Import) -> None:
        """Check import statements"""
        for alias in node.names:
            module_name = alias.name.split('.')[0]
            if module_name in FORBIDDEN_IMPORTS:
                self.violations.append(
                    f"Forbidden import detected: {alias.name} at line {node.lineno}"
                )
            self.imported_modules.add(module_name)
        self.generic_visit(node)
    
    def visit_ImportFrom(self, node: ast.ImportFrom) -> None:
        """Check from...import statements"""
        if node.module:
            module_name = node.module.split('.')[0]
            if module_name in FORBIDDEN_IMPORTS:
                self.violations.append(
                    f"Forbidden import detected: from {node.module} at line {node.lineno}"
                )
            self.imported_modules.add(module_name)
        self.generic_visit(node)
    
    def visit_Call(self, node: ast.Call) -> None:
        """Check function calls for dangerous builtins"""
        if isinstance(node.func, ast.Name):
            func_name = node.func.id
            if func_name in FORBIDDEN_BUILTINS:
                self.violations.append(
                    f"Forbidden builtin function: {func_name} at line {node.lineno}"
                )
        elif isinstance(node.func, ast.Attribute):
            # Check for getattr, setattr, etc.
            if node.func.attr in FORBIDDEN_BUILTINS:
                self.violations.append(
                    f"Forbidden attribute access: {node.func.attr} at line {node.lineno}"
                )
        self.generic_visit(node)
    
    def visit_Attribute(self, node: ast.Attribute) -> None:
        """Check attribute access for __import__, __builtins__, etc."""
        if node.attr.startswith('__') and node.attr.endswith('__'):
            if node.attr in ['__import__', '__builtins__', '__globals__', '__locals__']:
                self.violations.append(
                    f"Forbidden dunder attribute: {node.attr} at line {node.lineno}"
                )
        self.generic_visit(node)


def validate_code_with_ast(code: str) -> Dict[str, Any]:
    """
    Validate code using AST parsing for security checks.
    
    Args:
        code: The Python code to validate
    
    Returns:
        Dictionary with validation results:
        {
            "safe": bool,
            "violations": List[str],
            "error": Optional[str]
        }
    """
    result = {
        "safe": True,
        "violations": [],
        "error": None
    }
    
    try:
        # Parse the code into an AST
        tree = ast.parse(code)
        
        # Run security validator
        validator = ASTSecurityValidator()
        validator.visit(tree)
        
        if validator.violations:
            result["safe"] = False
            result["violations"] = validator.violations
    
    except SyntaxError as e:
        result["safe"] = False
        result["error"] = f"Syntax error: {str(e)}"
    
    except Exception as e:
        result["safe"] = False
        result["error"] = f"Validation error: {str(e)}"
    
    return result


def _execute_code_in_process(code: str, result_queue: multiprocessing.Queue) -> None:
    """
    Execute code in a separate process (used for timeout enforcement).
    
    Args:
        code: The code to execute
        result_queue: Queue to put the result in
    """
    stdout_buffer = io.StringIO()
    stderr_buffer = io.StringIO()
    
    result = {
        "success": False,
        "output": "",
        "error": None
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
                'round': round,
                'pow': pow,
                'divmod': divmod,
                'chr': chr,
                'ord': ord,
            }
        }
        
        # Redirect stdout and stderr
        with redirect_stdout(stdout_buffer), redirect_stderr(stderr_buffer):
            try:
                # Execute the code
                exec(code, namespace)
                result["success"] = True
                result["output"] = stdout_buffer.getvalue()
            
            except Exception as e:
                result["error"] = f"{type(e).__name__}: {str(e)}"
                result["output"] = stdout_buffer.getvalue()
        
        # Capture any stderr output
        stderr_output = stderr_buffer.getvalue()
        if stderr_output:
            result["error"] = (result["error"] or "") + "\n" + stderr_output
    
    except Exception as e:
        result["error"] = f"Execution error: {str(e)}"
    
    finally:
        # Clean up resources
        stdout_buffer.close()
        stderr_buffer.close()
    
    result_queue.put(result)


def execute_code_safely(code: str, timeout_seconds: Optional[int] = None) -> Dict[str, Any]:
    """
    Execute Python code safely with cross-platform timeout protection.
    Uses multiprocessing for timeout enforcement on all platforms including Windows.
    
    Args:
        code: The Python code to execute
        timeout_seconds: Maximum execution time in seconds (default: from config)
    
    Returns:
        Dictionary containing execution results:
        {
            "success": bool,
            "output": str,
            "error": str or None,
            "timeout": bool
        }
    """
    if timeout_seconds is None:
        timeout_seconds = CODE_EXECUTION_TIMEOUT
    
    # Validate input length
    if len(code) > MAX_CODE_LENGTH:
        return {
            "success": False,
            "output": "",
            "error": f"Code exceeds maximum length of {MAX_CODE_LENGTH} characters",
            "timeout": False
        }
    
    # Perform AST-based security validation
    validation_result = validate_code_with_ast(code)
    if not validation_result["safe"]:
        error_msg = "Security validation failed:\n"
        if validation_result["error"]:
            error_msg += validation_result["error"]
        if validation_result["violations"]:
            error_msg += "\n".join(validation_result["violations"])
        
        return {
            "success": False,
            "output": "",
            "error": error_msg,
            "timeout": False
        }
    
    # Create a queue for the result
    result_queue = multiprocessing.Queue()
    
    # Create and start the process
    process = multiprocessing.Process(
        target=_execute_code_in_process,
        args=(code, result_queue)
    )
    
    result = {
        "success": False,
        "output": "",
        "error": None,
        "timeout": False
    }
    
    try:
        process.start()
        process.join(timeout=timeout_seconds)
        
        if process.is_alive():
            # Timeout occurred
            process.terminate()
            process.join(timeout=1)
            if process.is_alive():
                process.kill()
                process.join()
            
            result["timeout"] = True
            result["error"] = f"Code execution exceeded {timeout_seconds} seconds timeout"
        else:
            # Process completed, get the result
            if not result_queue.empty():
                result = result_queue.get()
                result["timeout"] = False
            else:
                result["error"] = "Process completed but no result was returned"
    
    except Exception as e:
        result["error"] = f"Execution error: {str(e)}"
        if process.is_alive():
            process.terminate()
            process.join()
    
    finally:
        # Clean up
        result_queue.close()
        result_queue.join_thread()
    
    return result


def validate_test_cases(test_cases: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Validate test cases structure and content.
    
    Args:
        test_cases: List of test case dictionaries
    
    Returns:
        Dictionary with validation results:
        {
            "valid": bool,
            "errors": List[str]
        }
    """
    errors = []
    
    if not isinstance(test_cases, list):
        return {
            "valid": False,
            "errors": ["Test cases must be a list"]
        }
    
    if len(test_cases) == 0:
        return {
            "valid": False,
            "errors": ["At least one test case is required"]
        }
    
    if len(test_cases) > MAX_TEST_CASES:
        return {
            "valid": False,
            "errors": [f"Maximum {MAX_TEST_CASES} test cases allowed"]
        }
    
    for i, test_case in enumerate(test_cases, 1):
        if not isinstance(test_case, dict):
            errors.append(f"Test case {i}: Must be a dictionary")
            continue
        
        if "expected_output" not in test_case:
            errors.append(f"Test case {i}: Missing 'expected_output' field")
        
        if "input" not in test_case:
            errors.append(f"Test case {i}: Missing 'input' field")
    
    return {
        "valid": len(errors) == 0,
        "errors": errors
    }


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
            "overall_status": "passed" | "partial" | "failed" | "error"
        }
    """
    # Validate test cases first
    validation = validate_test_cases(test_cases)
    if not validation["valid"]:
        return {
            "passed": 0,
            "failed": 0,
            "total": 0,
            "test_results": [],
            "overall_status": "error",
            "error": "Invalid test cases: " + "; ".join(validation["errors"])
        }
    
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
        execution_result = execute_code_safely(test_code, timeout_seconds=CODE_EXECUTION_TIMEOUT)
        
        if execution_result["timeout"]:
            test_result["error"] = "Timeout"
            test_result["actual"] = "Code execution timed out"
            results["failed"] += 1
            
        elif execution_result["error"]:
            test_result["error"] = execution_result["error"]
            test_result["actual"] = execution_result["output"] or "No output"
            results["failed"] += 1
            
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
    Check if code contains potentially dangerous operations using AST analysis.
    
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
    validation_result = validate_code_with_ast(code)
    
    return {
        "safe": validation_result["safe"],
        "warnings": validation_result["violations"],
        "blocked_operations": validation_result["violations"]
    }


# Made with Bob