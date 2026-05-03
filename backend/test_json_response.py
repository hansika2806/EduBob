"""
Test script to verify test_cases is returned as JSON array
"""

import requests
import json

BASE_URL = "http://localhost:8000"

def test_assignment_json_format():
    """Test that assignment returns test_cases as JSON array"""
    print("\n=== Testing Assignment JSON Format ===")
    
    # Create Bob output with test cases
    bob_output = json.dumps({
        "title": "Test Assignment",
        "description": "Test description",
        "test_cases": [
            {
                "input": "print(1 + 1)",
                "expected_output": "2",
                "description": "Simple addition"
            },
            {
                "input": "print(2 * 3)",
                "expected_output": "6",
                "description": "Simple multiplication"
            }
        ],
        "starter_code": "# Write your code here",
        "hints": ["Use basic operators", "Remember order of operations"]
    })
    
    request_data = {
        "topic": "math",
        "difficulty": "beginner",
        "bob_output": bob_output
    }
    
    # Generate assignment
    response = requests.post(f"{BASE_URL}/api/assignments/generate", json=request_data)
    print(f"Status: {response.status_code}")
    
    if response.status_code == 201:
        data = response.json()
        print(f"\nResponse:")
        print(json.dumps(data, indent=2))
        
        # Check if test_cases is a list
        test_cases = data.get("test_cases")
        print(f"\ntest_cases type: {type(test_cases)}")
        print(f"test_cases is list: {isinstance(test_cases, list)}")
        
        if isinstance(test_cases, list):
            print("✅ SUCCESS: test_cases is returned as JSON array!")
            print(f"Number of test cases: {len(test_cases)}")
            for i, tc in enumerate(test_cases, 1):
                print(f"  Test case {i}: {tc.get('description')}")
        else:
            print("❌ FAILED: test_cases is still a string!")
            
        # Check hints
        hints = data.get("hints")
        print(f"\nhints type: {type(hints)}")
        print(f"hints is list: {isinstance(hints, list)}")
        
        if isinstance(hints, list):
            print("✅ SUCCESS: hints is returned as JSON array!")
        else:
            print("❌ FAILED: hints is still a string!")
    else:
        print(f"Error: {response.json()}")


if __name__ == "__main__":
    try:
        test_assignment_json_format()
    except requests.exceptions.ConnectionError:
        print("\n❌ ERROR: Cannot connect to server. Make sure the backend is running on port 8000.")
    except Exception as e:
        print(f"\n❌ ERROR: {str(e)}")
        import traceback
        traceback.print_exc()

# Made with Bob