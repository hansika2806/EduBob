"""
Phase 3 Testing: Code Review and Codebase Analysis

Tests the new Phase 3 endpoints:
- POST /api/review/spec-check
- POST /api/codebase/analyze
"""

import requests
import json

BASE_URL = "http://localhost:8000"


def test_code_review():
    """Test the code review endpoint"""
    print("\n" + "="*60)
    print("Testing Code Review Endpoint")
    print("="*60)
    
    # Sample student code
    student_code = """
def calculate_sum(numbers):
    total = 0
    for num in numbers:
        total = total + num
    return total

result = calculate_sum([1, 2, 3, 4, 5])
print(result)
"""
    
    # Sample assignment spec
    assignment_spec = """
Create a function that calculates the sum of numbers in a list.
Requirements:
- Function name: calculate_sum
- Input: List of numbers
- Output: Sum of all numbers
- Use efficient Python idioms
"""
    
    # Sample Bob IDE output (manually obtained)
    bob_output = """
Code Review Summary:
The code is functionally correct and produces the expected output.

Mistakes:
- Using a manual loop instead of Python's built-in sum() function
- Variable naming could be more descriptive

Improvement Suggestions:
- Use sum() function for better readability: return sum(numbers)
- Consider adding input validation for empty lists
- Add docstring to explain function purpose
- Use type hints for better code documentation
"""
    
    payload = {
        "student_code": student_code,
        "assignment_spec": assignment_spec,
        "bob_output": bob_output
    }
    
    try:
        response = requests.post(f"{BASE_URL}/api/review/spec-check", json=payload)
        print(f"\nStatus Code: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print("\n✅ Code Review Result:")
            print(f"\nSummary: {result['summary_feedback']}")
            print(f"\nMistakes Found ({len(result['mistakes'])}):")
            for i, mistake in enumerate(result['mistakes'], 1):
                print(f"  {i}. {mistake}")
            print(f"\nImprovement Suggestions ({len(result['improvement_suggestions'])}):")
            for i, suggestion in enumerate(result['improvement_suggestions'], 1):
                print(f"  {i}. {suggestion}")
        else:
            print(f"\n❌ Error: {response.text}")
            
    except requests.exceptions.ConnectionError:
        print("\n❌ Error: Could not connect to server. Make sure the API is running.")
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")


def test_codebase_analysis():
    """Test the codebase analysis endpoint"""
    print("\n" + "="*60)
    print("Testing Codebase Analysis Endpoint")
    print("="*60)
    
    # Sample repository URL (for reference only)
    repo_url = "https://github.com/example/sample-project"
    
    # Sample Bob IDE output (manually obtained from analyzing a codebase)
    bob_output = """
Architecture Summary:
This is a Flask-based web application with a modular structure.
The project follows MVC pattern with clear separation of concerns.

Key Files:
- app.py: Main application entry point and route definitions
- models.py: Database models using SQLAlchemy ORM
- config.py: Configuration management for different environments
- requirements.txt: Python dependencies list

Tech Stack:
- Flask (Web Framework)
- SQLAlchemy (ORM)
- PostgreSQL (Database)
- Jinja2 (Templating)
- pytest (Testing)

Explanation:
The application uses a standard Flask project structure with blueprints
for modular organization. Database interactions are handled through
SQLAlchemy ORM, providing database-agnostic code. The configuration
system supports multiple environments (development, testing, production).
"""
    
    payload = {
        "repo_url": repo_url,
        "bob_output": bob_output
    }
    
    try:
        response = requests.post(f"{BASE_URL}/api/codebase/analyze", json=payload)
        print(f"\nStatus Code: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print("\n✅ Codebase Analysis Result:")
            print(f"\nArchitecture: {result['architecture_summary']}")
            print(f"\nKey Files ({len(result['key_files'])}):")
            for file_info in result['key_files']:
                print(f"  - {file_info['file']}: {file_info['purpose']}")
            print(f"\nTech Stack ({len(result['tech_stack'])}):")
            for tech in result['tech_stack']:
                print(f"  - {tech}")
            print(f"\nExplanation: {result['explanation']}")
        else:
            print(f"\n❌ Error: {response.text}")
            
    except requests.exceptions.ConnectionError:
        print("\n❌ Error: Could not connect to server. Make sure the API is running.")
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")


def test_review_with_minimal_bob_output():
    """Test review endpoint with minimal Bob output"""
    print("\n" + "="*60)
    print("Testing Review with Minimal Bob Output")
    print("="*60)
    
    payload = {
        "student_code": "def add(a, b): return a + b",
        "assignment_spec": "Create an add function",
        "bob_output": "The code looks good and works correctly."
    }
    
    try:
        response = requests.post(f"{BASE_URL}/api/review/spec-check", json=payload)
        print(f"\nStatus Code: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print("\n✅ Review Result (Minimal Output):")
            print(json.dumps(result, indent=2))
        else:
            print(f"\n❌ Error: {response.text}")
            
    except requests.exceptions.ConnectionError:
        print("\n❌ Error: Could not connect to server.")
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")


def main():
    """Run all Phase 3 tests"""
    print("\n" + "="*60)
    print("PHASE 3 TESTING: Code Review & Codebase Analysis")
    print("="*60)
    print("\nMake sure the API server is running: python backend/main.py")
    print("Press Enter to continue...")
    input()
    
    # Run tests
    test_code_review()
    test_codebase_analysis()
    test_review_with_minimal_bob_output()
    
    print("\n" + "="*60)
    print("Phase 3 Testing Complete!")
    print("="*60)


if __name__ == "__main__":
    main()

# Made with Bob