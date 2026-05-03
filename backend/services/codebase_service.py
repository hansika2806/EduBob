"""
Codebase Analysis Service

Analyzes repository structure and provides architectural insights.
Uses Bob IDE output (manually provided) for intelligent analysis.
"""

from typing import Dict, Any, List


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
    
    # Extract architecture summary from Bob output
    lines = bob_output.split('\n')
    
    # Look for architecture/structure section
    architecture_lines = []
    in_architecture = False
    
    for line in lines:
        line_lower = line.lower()
        
        if "architecture" in line_lower or "structure" in line_lower or "overview" in line_lower:
            in_architecture = True
            continue
        
        if in_architecture:
            if line.startswith('#') and len(architecture_lines) > 0:
                break
            if line.strip() and not line.startswith('-') and not line.startswith('*'):
                architecture_lines.append(line.strip())
    
    result["architecture_summary"] = ' '.join(architecture_lines) if architecture_lines else "Repository structure analyzed."
    
    # Extract key files from Bob output
    in_files_section = False
    for line in lines:
        line_lower = line.lower()
        
        if "key file" in line_lower or "important file" in line_lower or "main file" in line_lower:
            in_files_section = True
            continue
        
        if in_files_section:
            if line.startswith('-') or line.startswith('*') or line.startswith('•'):
                # Parse file entry: "- filename: purpose"
                file_entry = line.lstrip('-*• ').strip()
                if ':' in file_entry:
                    parts = file_entry.split(':', 1)
                    result["key_files"].append({
                        "file": parts[0].strip(),
                        "purpose": parts[1].strip()
                    })
                elif file_entry:
                    result["key_files"].append({
                        "file": file_entry,
                        "purpose": "Core component"
                    })
            elif line.startswith('#'):
                in_files_section = False
    
    # Extract tech stack from Bob output
    in_tech_section = False
    for line in lines:
        line_lower = line.lower()
        
        if "tech" in line_lower or "stack" in line_lower or "technolog" in line_lower or "framework" in line_lower:
            in_tech_section = True
            continue
        
        if in_tech_section:
            if line.startswith('-') or line.startswith('*') or line.startswith('•'):
                tech = line.lstrip('-*• ').strip()
                if tech:
                    result["tech_stack"].append(tech)
            elif line.startswith('#'):
                in_tech_section = False
    
    # Extract explanation/summary
    explanation_lines = []
    in_explanation = False
    
    for line in lines:
        line_lower = line.lower()
        
        if "explanation" in line_lower or "summary" in line_lower or "description" in line_lower:
            in_explanation = True
            continue
        
        if in_explanation:
            if line.startswith('#') and len(explanation_lines) > 0:
                break
            if line.strip():
                explanation_lines.append(line.strip())
    
    result["explanation"] = ' '.join(explanation_lines) if explanation_lines else "Codebase analysis completed based on Bob IDE session."
    
    # Fallback: if no structured data found
    if not result["key_files"]:
        result["key_files"] = [
            {
                "file": "See Bob IDE output",
                "purpose": "Detailed file analysis available in Bob session"
            }
        ]
    
    if not result["tech_stack"]:
        result["tech_stack"] = ["See Bob IDE output for tech stack details"]
    
    if not result["architecture_summary"]:
        result["architecture_summary"] = "Repository analysis completed. Check Bob IDE output for details."
    
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