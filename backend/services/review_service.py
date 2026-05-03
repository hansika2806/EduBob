"""
Code Review Service

Analyzes student submissions against assignment specifications.
Uses Bob IDE output (manually provided) for intelligent feedback.
"""

from typing import Dict, Any, List
import json
import re


def analyze_submission(
    student_code: str,
    assignment_spec: str,
    bob_output: str
) -> Dict[str, Any]:
    """
    Analyze student submission against assignment specification.
    
    Args:
        student_code: The student's submitted code
        assignment_spec: Assignment specification (string or JSON)
        bob_output: Bob IDE output is passed here from manual Ask mode session
    
    Returns:
        Dictionary containing review feedback:
        {
            "summary_feedback": str,
            "mistakes": List[str],
            "improvement_suggestions": List[str]
        }
    
    Note:
        Bob IDE output is passed here from manual Ask mode session.
        This function does NOT call Bob via subprocess or CLI.
    """
    result = {
        "summary_feedback": "",
        "mistakes": [],
        "improvement_suggestions": []
    }
    
    # PRIORITY 1: Try JSON parsing
    try:
        json_data = json.loads(bob_output)
        if isinstance(json_data, dict):
            if "summary_feedback" in json_data:
                result["summary_feedback"] = json_data["summary_feedback"]
            if "mistakes" in json_data and isinstance(json_data["mistakes"], list):
                result["mistakes"] = json_data["mistakes"]
            if "improvement_suggestions" in json_data and isinstance(json_data["improvement_suggestions"], list):
                result["improvement_suggestions"] = json_data["improvement_suggestions"]
            
            # If we got valid data from JSON, return it
            if result["summary_feedback"] or result["mistakes"] or result["improvement_suggestions"]:
                return result
    except (json.JSONDecodeError, ValueError):
        pass
    
    # PRIORITY 2: Flexible text parsing
    lines = bob_output.split('\n')
    
    # Extract summary feedback
    summary_lines = []
    in_summary = False
    summary_keywords = ["summary", "feedback", "overall", "review"]
    
    for i, line in enumerate(lines):
        line_lower = line.lower()
        
        # Check if this line is a summary header
        if any(keyword in line_lower for keyword in summary_keywords):
            if ":" in line:
                # Extract content after colon on same line
                content = line.split(":", 1)[1].strip()
                if content:
                    summary_lines.append(content)
                in_summary = True
                continue
            else:
                in_summary = True
                continue
        
        if in_summary:
            # Stop at next section header
            if line.strip() and (line.endswith(":") or line.startswith("#")):
                break
            if line.strip():
                summary_lines.append(line.strip())
    
    if summary_lines:
        result["summary_feedback"] = " ".join(summary_lines)
    
    # Extract mistakes
    mistakes_keywords = ["mistake", "issue", "problem", "error"]
    in_mistakes = False
    
    for i, line in enumerate(lines):
        line_lower = line.lower()
        
        # Check if this line is a mistakes header
        if any(keyword in line_lower for keyword in mistakes_keywords):
            in_mistakes = True
            # Check if content is on same line after colon
            if ":" in line:
                content = line.split(":", 1)[1].strip()
                if content and not content.startswith("-") and not content.startswith("*"):
                    result["mistakes"].append(content)
            continue
        
        if in_mistakes:
            # Stop at next section header
            if line.strip() and (line.endswith(":") or line.startswith("#")):
                in_mistakes = False
                continue
            
            # Extract list items
            stripped = line.strip()
            if stripped:
                # Remove bullets, numbers, arrows
                item = re.sub(r'^[-*•→\d+\.]\s*', '', stripped)
                if item:
                    result["mistakes"].append(item)
    
    # Extract improvement suggestions
    suggestions_keywords = ["suggestion", "recommendation", "improve", "consider", "should"]
    in_suggestions = False
    
    for i, line in enumerate(lines):
        line_lower = line.lower()
        
        # Check if this line is a suggestions header
        if any(keyword in line_lower for keyword in suggestions_keywords):
            in_suggestions = True
            # Check if content is on same line after colon
            if ":" in line:
                content = line.split(":", 1)[1].strip()
                if content and not content.startswith("-") and not content.startswith("*"):
                    result["improvement_suggestions"].append(content)
            continue
        
        if in_suggestions:
            # Stop at next section header
            if line.strip() and (line.endswith(":") or line.startswith("#")):
                in_suggestions = False
                continue
            
            # Extract list items
            stripped = line.strip()
            if stripped:
                # Remove bullets, numbers, arrows
                item = re.sub(r'^[-*•→\d+\.]\s*', '', stripped)
                if item:
                    result["improvement_suggestions"].append(item)
    
    # PRIORITY 3: Fallback - extract meaningful content
    if not result["summary_feedback"] and not result["mistakes"] and not result["improvement_suggestions"]:
        # Use first 300 characters as summary
        result["summary_feedback"] = bob_output[:300].strip()
        result["mistakes"] = []
        result["improvement_suggestions"] = []
    
    return result


def parse_bob_review_output(bob_output: str) -> Dict[str, Any]:
    """
    Parse Bob IDE output into structured review data.
    
    Args:
        bob_output: Raw output from Bob IDE review session
    
    Returns:
        Structured review data
    """
    return analyze_submission("", "", bob_output)


# Made with Bob