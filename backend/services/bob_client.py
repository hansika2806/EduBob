"""
Bob IDE Client Service

This service handles integration with Bob IDE outputs.
IMPORTANT: This does NOT use subprocess or CLI.
Each function accepts Bob IDE output that was manually generated and pasted.
"""

import json
from typing import Dict, Any, List


def generate_assignment(bob_output: str, topic: str, difficulty: str) -> Dict[str, Any]:
    """
    Parse Bob IDE output for assignment generation.
    
    Args:
        bob_output: The raw output from Bob IDE (pasted manually from a Bob session)
        topic: The programming topic (e.g., "loops", "functions", "data structures")
        difficulty: The difficulty level (e.g., "beginner", "intermediate", "advanced")
    
    Returns:
        Structured assignment data as a dictionary
    
    Example Bob IDE output format expected:
    {
        "title": "Assignment Title",
        "description": "Assignment description...",
        "test_cases": [
            {
                "input": "test input",
                "expected_output": "expected result",
                "description": "what this test checks"
            }
        ],
        "starter_code": "def function_name():\n    pass",
        "hints": ["hint 1", "hint 2"]
    }
    """
    try:
        # Bob IDE output is passed here from manual session
        # Parse the JSON output from Bob
        parsed_output = json.loads(bob_output)
        
        # Structure the assignment data
        assignment_data = {
            "title": parsed_output.get("title", f"{topic.title()} - {difficulty.title()}"),
            "description": parsed_output.get("description", ""),
            "test_cases": json.dumps(parsed_output.get("test_cases", [])),
            "starter_code": parsed_output.get("starter_code", ""),
            "hints": parsed_output.get("hints", []),
            "topic": topic,
            "difficulty": difficulty
        }
        
        return assignment_data
        
    except json.JSONDecodeError as e:
        # If Bob output is not JSON, try to extract structured data
        return {
            "title": f"{topic.title()} - {difficulty.title()}",
            "description": bob_output,
            "test_cases": json.dumps([]),
            "starter_code": "",
            "hints": [],
            "topic": topic,
            "difficulty": difficulty,
            "parse_error": str(e)
        }


def analyze_code(bob_output: str, code: str, spec: str) -> Dict[str, Any]:
    """
    Parse Bob IDE output for code analysis.
    
    Args:
        bob_output: The raw output from Bob IDE (pasted manually from a Bob session)
        code: The student's submitted code
        spec: The assignment specification/requirements
    
    Returns:
        Analysis results as a dictionary
    
    Example Bob IDE output format expected:
    {
        "correctness": "correct|incorrect|partial",
        "issues": [
            {
                "line": 5,
                "type": "logic_error|syntax_error|style_issue",
                "message": "Description of the issue",
                "suggestion": "How to fix it"
            }
        ],
        "strengths": ["what the student did well"],
        "improvements": ["what could be better"],
        "score": 85
    }
    """
    try:
        # Bob IDE output is passed here from manual session
        # Parse the JSON output from Bob
        parsed_output = json.loads(bob_output)
        
        # Structure the analysis data
        analysis_data = {
            "correctness": parsed_output.get("correctness", "unknown"),
            "issues": parsed_output.get("issues", []),
            "strengths": parsed_output.get("strengths", []),
            "improvements": parsed_output.get("improvements", []),
            "score": parsed_output.get("score", 0),
            "feedback": parsed_output.get("feedback", ""),
            "code_analyzed": code[:100] + "..." if len(code) > 100 else code
        }
        
        return analysis_data
        
    except json.JSONDecodeError as e:
        # If Bob output is not JSON, return raw feedback
        return {
            "correctness": "unknown",
            "issues": [],
            "strengths": [],
            "improvements": [],
            "score": 0,
            "feedback": bob_output,
            "parse_error": str(e)
        }


def analyze_repo(bob_output: str, repo_url: str) -> Dict[str, Any]:
    """
    Parse Bob IDE output for repository analysis.
    
    Args:
        bob_output: The raw output from Bob IDE (pasted manually from a Bob session)
        repo_url: The URL of the repository to analyze
    
    Returns:
        Repository analysis results as a dictionary
    
    Example Bob IDE output format expected:
    {
        "structure": {
            "files": ["list of files"],
            "directories": ["list of directories"],
            "main_language": "Python"
        },
        "code_quality": {
            "score": 75,
            "issues": ["list of issues"],
            "suggestions": ["list of suggestions"]
        },
        "patterns": {
            "common_mistakes": ["list of common mistakes found"],
            "good_practices": ["list of good practices found"]
        }
    }
    """
    try:
        # Bob IDE output is passed here from manual session
        # Parse the JSON output from Bob
        parsed_output = json.loads(bob_output)
        
        # Structure the repository analysis data
        repo_analysis = {
            "repo_url": repo_url,
            "structure": parsed_output.get("structure", {}),
            "code_quality": parsed_output.get("code_quality", {}),
            "patterns": parsed_output.get("patterns", {}),
            "summary": parsed_output.get("summary", ""),
            "recommendations": parsed_output.get("recommendations", [])
        }
        
        return repo_analysis
        
    except json.JSONDecodeError as e:
        # If Bob output is not JSON, return raw analysis
        return {
            "repo_url": repo_url,
            "structure": {},
            "code_quality": {},
            "patterns": {},
            "summary": bob_output,
            "parse_error": str(e)
        }


def parse_test_cases(test_cases_json: str) -> List[Dict[str, Any]]:
    """
    Helper function to parse test cases from JSON string.
    
    Args:
        test_cases_json: JSON string containing test cases
    
    Returns:
        List of test case dictionaries
    """
    try:
        return json.loads(test_cases_json)
    except (json.JSONDecodeError, TypeError):
        return []


# Made with Bob