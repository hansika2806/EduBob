"""
Codebase Analysis Service

Analyzes repository structure and provides architectural insights.
Uses Bob IDE output (manually provided) for intelligent analysis.
"""

from typing import Dict, Any, List
import json
import re


def analyze_repo(repo_url: str, bob_output: str) -> Dict[str, Any]:
    """
    Analyze repository structure and architecture.
    
    Args:
        repo_url: Repository URL (stored for reference only, not cloned)
        bob_output: Bob IDE output contains full analysis from manual session
    
    Returns:
        Dictionary containing codebase analysis:
        {
            "architecture_summary": str,
            "key_files": List[Dict[str, str]],
            "tech_stack": List[str],
            "explanation": str
        }
    
    Note:
        This function does NOT clone the repository or install gitpython.
        Bob IDE output is passed here from manual Ask mode session.
        The repo_url is only stored for reference.
    """
    result = {
        "architecture_summary": "",
        "key_files": [],
        "tech_stack": [],
        "explanation": ""
    }
    
    # PRIORITY 1: Try JSON parsing
    try:
        json_data = json.loads(bob_output)
        if isinstance(json_data, dict):
            if "architecture_summary" in json_data:
                result["architecture_summary"] = json_data["architecture_summary"]
            if "key_files" in json_data and isinstance(json_data["key_files"], list):
                result["key_files"] = json_data["key_files"]
            if "tech_stack" in json_data and isinstance(json_data["tech_stack"], list):
                result["tech_stack"] = json_data["tech_stack"]
            if "explanation" in json_data:
                result["explanation"] = json_data["explanation"]
            
            # If we got valid data from JSON, return it
            if result["architecture_summary"] or result["key_files"] or result["tech_stack"] or result["explanation"]:
                return result
    except (json.JSONDecodeError, ValueError):
        pass
    
    # PRIORITY 2: Flexible text parsing
    lines = bob_output.split('\n')
    
    # Extract architecture summary
    architecture_lines = []
    in_architecture = False
    architecture_keywords = ["architecture", "project structure", "overview", "structure"]
    
    for i, line in enumerate(lines):
        line_lower = line.lower()
        
        # Check if this line is an architecture header
        if any(keyword in line_lower for keyword in architecture_keywords):
            if ":" in line:
                # Extract content after colon on same line
                content = line.split(":", 1)[1].strip()
                if content:
                    architecture_lines.append(content)
                in_architecture = True
                continue
            else:
                in_architecture = True
                continue
        
        if in_architecture:
            # Stop at next section header
            if line.strip() and (line.endswith(":") or line.startswith("#")):
                break
            if line.strip() and not line.startswith("-") and not line.startswith("*") and not line.startswith("•"):
                architecture_lines.append(line.strip())
    
    if architecture_lines:
        result["architecture_summary"] = " ".join(architecture_lines)
    
    # Extract key files
    files_keywords = ["key file", "important file", "main file", "files", "components"]
    in_files = False
    
    for i, line in enumerate(lines):
        line_lower = line.lower()
        
        # Check if this line is a files header
        if any(keyword in line_lower for keyword in files_keywords):
            in_files = True
            continue
        
        if in_files:
            # Stop at next section header
            if line.strip() and (line.endswith(":") or line.startswith("#")):
                in_files = False
                continue
            
            # Extract list items
            stripped = line.strip()
            if stripped:
                # Remove bullets, numbers, arrows
                item = re.sub(r'^[-*•→\d+\.]\s*', '', stripped)
                if item:
                    # Try to parse "filename: purpose" format
                    if ":" in item:
                        parts = item.split(":", 1)
                        result["key_files"].append({
                            "file": parts[0].strip(),
                            "purpose": parts[1].strip()
                        })
                    else:
                        result["key_files"].append({
                            "file": item,
                            "purpose": "Core component"
                        })
    
    # Extract tech stack
    tech_keywords = ["tech", "stack", "technolog", "framework", "libraries", "dependencies"]
    in_tech = False
    
    for i, line in enumerate(lines):
        line_lower = line.lower()
        
        # Check if this line is a tech stack header
        if any(keyword in line_lower for keyword in tech_keywords):
            in_tech = True
            continue
        
        if in_tech:
            # Stop at next section header
            if line.strip() and (line.endswith(":") or line.startswith("#")):
                in_tech = False
                continue
            
            # Extract list items
            stripped = line.strip()
            if stripped:
                # Remove bullets, numbers, arrows
                item = re.sub(r'^[-*•→\d+\.]\s*', '', stripped)
                if item:
                    result["tech_stack"].append(item)
    
    # Extract explanation
    explanation_lines = []
    in_explanation = False
    explanation_keywords = ["explanation", "description", "summary", "details"]
    
    for i, line in enumerate(lines):
        line_lower = line.lower()
        
        # Check if this line is an explanation header
        if any(keyword in line_lower for keyword in explanation_keywords):
            if ":" in line:
                # Extract content after colon on same line
                content = line.split(":", 1)[1].strip()
                if content:
                    explanation_lines.append(content)
                in_explanation = True
                continue
            else:
                in_explanation = True
                continue
        
        if in_explanation:
            # Stop at next section header
            if line.strip() and (line.endswith(":") or line.startswith("#")):
                break
            if line.strip() and not line.startswith("-") and not line.startswith("*") and not line.startswith("•"):
                explanation_lines.append(line.strip())
    
    if explanation_lines:
        result["explanation"] = " ".join(explanation_lines)
    
    # PRIORITY 3: Fallback - extract meaningful content
    if not result["architecture_summary"] and not result["key_files"] and not result["tech_stack"] and not result["explanation"]:
        # Use first 300 characters as architecture summary
        result["architecture_summary"] = bob_output[:300].strip()
        result["key_files"] = []
        result["tech_stack"] = []
        result["explanation"] = ""
    
    return result


def parse_bob_codebase_output(bob_output: str) -> Dict[str, Any]:
    """
    Parse Bob IDE output into structured codebase analysis.
    
    Args:
        bob_output: Raw output from Bob IDE codebase analysis session
    
    Returns:
        Structured codebase analysis data
    """
    return analyze_repo("", bob_output)


# Made with Bob