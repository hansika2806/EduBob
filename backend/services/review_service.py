"""
Code Review Service

Analyzes student submissions against assignment specifications.
Uses Bob IDE output (manually provided) for intelligent feedback.
"""

from typing import Dict, Any, List


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
    # Parse Bob IDE output to extract review feedback
    # Bob IDE output contains the analysis from a manual session
    
    result = {
        "summary_feedback": "",
        "mistakes": [],
        "improvement_suggestions": []
    }
    
    # Extract summary feedback from Bob output
    if "summary" in bob_output.lower() or "feedback" in bob_output.lower():
        lines = bob_output.split('\n')
        summary_lines = []
        in_summary = False
        
        for line in lines:
            line_lower = line.lower()
            if "summary" in line_lower or "overall" in line_lower:
                in_summary = True
                continue
            if in_summary and line.strip():
                if line.startswith('#') or line.startswith('##'):
                    break
                summary_lines.append(line.strip())
        
        result["summary_feedback"] = ' '.join(summary_lines) if summary_lines else "Code review completed."
    else:
        result["summary_feedback"] = "Code review completed based on Bob IDE analysis."
    
    # Extract mistakes from Bob output
    mistakes_section = False
    for line in bob_output.split('\n'):
        line_lower = line.lower()
        
        if "mistake" in line_lower or "error" in line_lower or "issue" in line_lower:
            mistakes_section = True
            continue
        
        if mistakes_section:
            if line.startswith('-') or line.startswith('*') or line.startswith('•'):
                mistake = line.lstrip('-*• ').strip()
                if mistake:
                    result["mistakes"].append(mistake)
            elif line.startswith('#') or (line.strip() and not line.startswith(' ')):
                mistakes_section = False
    
    # Extract improvement suggestions from Bob output
    suggestions_section = False
    for line in bob_output.split('\n'):
        line_lower = line.lower()
        
        if "suggestion" in line_lower or "improve" in line_lower or "recommend" in line_lower:
            suggestions_section = True
            continue
        
        if suggestions_section:
            if line.startswith('-') or line.startswith('*') or line.startswith('•'):
                suggestion = line.lstrip('-*• ').strip()
                if suggestion:
                    result["improvement_suggestions"].append(suggestion)
            elif line.startswith('#') or (line.strip() and not line.startswith(' ')):
                suggestions_section = False
    
    # Fallback: if no structured data found, provide basic feedback
    if not result["mistakes"] and not result["improvement_suggestions"]:
        result["summary_feedback"] = "Review completed. Please check Bob IDE output for detailed analysis."
        result["mistakes"] = ["No specific mistakes identified in Bob output"]
        result["improvement_suggestions"] = ["Refer to Bob IDE session for detailed suggestions"]
    
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