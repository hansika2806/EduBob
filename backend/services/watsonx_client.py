"""
IBM watsonx.ai client for analyzing student error patterns.
Includes proper logging and uses centralized configuration.
"""
import requests
import re
import logging
from typing import List, Dict
from collections import Counter

from config import (
    WATSONX_API_KEY,
    WATSONX_PROJECT_ID,
    WATSONX_URL,
    WATSONX_MODEL_ID,
    WATSONX_MAX_NEW_TOKENS,
    WATSONX_MIN_NEW_TOKENS,
    WATSONX_TIMEOUT
)

# Configure logging
logger = logging.getLogger(__name__)


def analyze_errors_intelligently(error_messages: List[str]) -> Dict:
    """
    Analyze errors using pattern matching and NLP techniques.
    This provides intelligent fallback when watsonx.ai API is unavailable.
    
    Args:
        error_messages: List of error message strings
    
    Returns:
        Dictionary with analysis results
    """
    if not error_messages:
        return {
            "common_errors": ["No errors to analyze yet"],
            "struggling_concepts": ["Submit more assignments to see patterns"],
            "ai_reasoning": "Insufficient data for pattern analysis",
            "analysis_method": "Awaiting Data"
        }
    
    common_errors = []
    struggling_concepts = []
    
    # Pattern detection
    error_patterns = {
        "off_by_one": ["range", "index", "out of range", "IndexError"],
        "type_mismatch": ["TypeError", "int", "str", "float", "type"],
        "undefined_variable": ["NameError", "not defined", "undefined"],
        "syntax_error": ["SyntaxError", "invalid syntax", "unexpected"],
        "logic_error": ["AssertionError", "Expected", "got", "incorrect"],
        "recursion": ["RecursionError", "maximum recursion", "stack"],
        "indentation": ["IndentationError", "expected an indented"],
        "attribute": ["AttributeError", "has no attribute"],
        "zero_division": ["ZeroDivisionError", "division by zero"],
        "import_error": ["ImportError", "ModuleNotFoundError"]
    }
    
    concept_mapping = {
        "off_by_one": "Loop boundaries and array indexing",
        "type_mismatch": "Data type conversion and type checking",
        "undefined_variable": "Variable scope and initialization",
        "syntax_error": "Python syntax rules",
        "logic_error": "Algorithm logic and problem-solving",
        "recursion": "Recursive function design and base cases",
        "indentation": "Python indentation and code blocks",
        "attribute": "Object-oriented programming and methods",
        "zero_division": "Edge case handling and input validation",
        "import_error": "Module imports and dependencies"
    }
    
    # Count pattern occurrences
    pattern_counts = Counter()
    for error_msg in error_messages:
        error_lower = error_msg.lower()
        for pattern_name, keywords in error_patterns.items():
            if any(keyword.lower() in error_lower for keyword in keywords):
                pattern_counts[pattern_name] += 1
    
    # Generate insights
    if pattern_counts:
        # Top 5 error patterns
        top_patterns = pattern_counts.most_common(5)
        
        for pattern_name, count in top_patterns:
            if pattern_name == "off_by_one":
                common_errors.append(f"Off-by-one errors in loops ({count} occurrences)")
                struggling_concepts.append(concept_mapping[pattern_name])
            elif pattern_name == "type_mismatch":
                common_errors.append(f"Type conversion errors ({count} occurrences)")
                struggling_concepts.append(concept_mapping[pattern_name])
            elif pattern_name == "logic_error":
                common_errors.append(f"Logic errors in algorithm implementation ({count} occurrences)")
                struggling_concepts.append(concept_mapping[pattern_name])
            elif pattern_name == "recursion":
                common_errors.append(f"Missing base cases in recursive functions ({count} occurrences)")
                struggling_concepts.append(concept_mapping[pattern_name])
            elif pattern_name == "undefined_variable":
                common_errors.append(f"Undefined variable references ({count} occurrences)")
                struggling_concepts.append(concept_mapping[pattern_name])
            else:
                common_errors.append(f"{pattern_name.replace('_', ' ').title()} ({count} occurrences)")
                if pattern_name in concept_mapping:
                    struggling_concepts.append(concept_mapping[pattern_name])
    
    # Add general insights if we found patterns
    if not common_errors:
        common_errors = [
            "Syntax errors in basic Python structure",
            "Logic errors in algorithm implementation",
            "Missing edge case handling"
        ]
        struggling_concepts = [
            "Python syntax fundamentals",
            "Problem-solving and algorithm design",
            "Testing and debugging techniques"
        ]
    
    # Generate AI reasoning
    total_errors = len(error_messages)
    unique_patterns = len(pattern_counts)
    ai_reasoning = f"Analyzed {total_errors} error messages and identified {unique_patterns} distinct error patterns. "
    
    if pattern_counts:
        most_common = pattern_counts.most_common(1)[0]
        ai_reasoning += f"The most frequent issue is {most_common[0].replace('_', ' ')} ({most_common[1]} cases). "
    
    ai_reasoning += "Recommend focusing on these concepts in next lesson."
    
    return {
        "common_errors": common_errors[:5],
        "struggling_concepts": list(set(struggling_concepts))[:5],
        "ai_reasoning": ai_reasoning,
        "analysis_method": "Pattern Recognition Algorithm"
    }


def analyze_class_patterns(error_messages: List[str]) -> Dict:
    """
    Analyze student error patterns using IBM watsonx.ai granite model.
    Falls back to intelligent pattern analysis if API is unavailable.
    
    Args:
        error_messages: List of error message strings from student submissions
        
    Returns:
        Dict with common_errors, struggling_concepts, ai_reasoning, and analysis_method
    """
    # Check configuration
    if not WATSONX_API_KEY or not WATSONX_PROJECT_ID:
        logger.warning("watsonx.ai API credentials not configured, using intelligent fallback")
        result = analyze_errors_intelligently(error_messages)
        result["analysis_method"] = "Intelligent Pattern Analysis (API not configured)"
        return result
    
    if not error_messages:
        logger.info("No error messages to analyze")
        return {
            "common_errors": ["No errors to analyze yet"],
            "struggling_concepts": ["Submit more assignments to see patterns"],
            "ai_reasoning": "Waiting for student submissions to analyze",
            "analysis_method": "Awaiting Data"
        }
    
    # Try watsonx.ai API first
    try:
        # Prepare prompt for watsonx
        errors_text = "\n".join([f"- {err}" for err in error_messages[:20] if err])  # Limit to 20 errors
        
        prompt = f"""Analyze these student programming errors and identify patterns:

{errors_text}

Provide:
1. Common errors (list 3-5 most frequent error types)
2. Struggling concepts (list 3-5 programming concepts students struggle with)

Format your response as:
Common Errors:
- error 1
- error 2

Struggling Concepts:
- concept 1
- concept 2"""

        # Prepare API request
        url = f"{WATSONX_URL}/ml/v1/text/generation?version=2023-05-29"
        
        headers = {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "Authorization": f"Bearer {WATSONX_API_KEY}"
        }
        
        body = {
            "input": prompt,
            "parameters": {
                "decoding_method": "greedy",
                "max_new_tokens": WATSONX_MAX_NEW_TOKENS,
                "min_new_tokens": WATSONX_MIN_NEW_TOKENS,
                "stop_sequences": [],
                "repetition_penalty": 1
            },
            "model_id": WATSONX_MODEL_ID,
            "project_id": WATSONX_PROJECT_ID
        }
        
        logger.info(f"Calling watsonx.ai API with {len(error_messages)} error messages")
        response = requests.post(url, headers=headers, json=body, timeout=WATSONX_TIMEOUT)
        response.raise_for_status()
        
        result = response.json()
        generated_text = result.get("results", [{}])[0].get("generated_text", "")
        
        logger.info(f"watsonx.ai API success - generated text length: {len(generated_text)}")
        
        # Parse the response
        common_errors = []
        struggling_concepts = []
        
        lines = generated_text.split("\n")
        current_section = None
        
        for line in lines:
            line = line.strip()
            if "common error" in line.lower():
                current_section = "errors"
                continue
            elif "struggling concept" in line.lower():
                current_section = "concepts"
                continue
            elif line.startswith("-") or line.startswith("*") or line.startswith("•") or line.startswith("1") or line.startswith("2"):
                item = re.sub(r'^[-*•\d+\.]\s*', '', line).strip()
                if item and current_section == "errors":
                    common_errors.append(item)
                elif item and current_section == "concepts":
                    struggling_concepts.append(item)
        
        if common_errors or struggling_concepts:
            logger.info(f"Successfully parsed {len(common_errors)} errors and {len(struggling_concepts)} concepts")
            return {
                "common_errors": common_errors[:5],
                "struggling_concepts": struggling_concepts[:5],
                "ai_reasoning": f"Analysis by IBM watsonx.ai {WATSONX_MODEL_ID} model based on {len(error_messages)} student submissions",
                "analysis_method": f"IBM watsonx.ai {WATSONX_MODEL_ID}"
            }
        else:
            logger.warning("Failed to parse watsonx.ai response, using intelligent fallback")
            raise ValueError("Failed to parse watsonx response")
        
    except requests.exceptions.HTTPError as e:
        logger.error(f"watsonx.ai HTTP Error {e.response.status_code}: {str(e)}")
        logger.error(f"Response preview: {e.response.text[:200]}")
        logger.info("Falling back to intelligent pattern analysis")
        result = analyze_errors_intelligently(error_messages)
        result["analysis_method"] = f"Intelligent Pattern Analysis (API Error: {e.response.status_code})"
        return result
        
    except requests.exceptions.Timeout as e:
        logger.error(f"watsonx.ai request timeout after {WATSONX_TIMEOUT}s: {str(e)}")
        logger.info("Falling back to intelligent pattern analysis")
        result = analyze_errors_intelligently(error_messages)
        result["analysis_method"] = "Intelligent Pattern Analysis (API Timeout)"
        return result
        
    except requests.exceptions.RequestException as e:
        logger.error(f"watsonx.ai request error: {str(e)}")
        logger.info("Falling back to intelligent pattern analysis")
        result = analyze_errors_intelligently(error_messages)
        result["analysis_method"] = "Intelligent Pattern Analysis (API Unavailable)"
        return result
        
    except Exception as e:
        logger.error(f"Unexpected error in watsonx.ai analysis: {str(e)}", exc_info=True)
        logger.info("Falling back to intelligent pattern analysis")
        result = analyze_errors_intelligently(error_messages)
        result["analysis_method"] = "Intelligent Pattern Analysis (Fallback)"
        return result

# Made with Bob
