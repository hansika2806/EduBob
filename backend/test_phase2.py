"""
Phase 2 Testing Script

Tests the assignment system with Bob IDE integration.
"""

import requests
import json

BASE_URL = "http://localhost:8000"

def test_health():
    """Test health endpoint"""
    print("\n=== Testing Health Endpoint ===")
    response = requests.get(f"{BASE_URL}/health")
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    return response.status_code == 200


def test_create_student():
    """Create a test student"""
    print("\n=== Creating Test Student ===")
    student_data = {
        "name": "Alice Johnson",
        "email": "alice@example.com",
        "role": "student"
    }
    response = requests.post(f"{BASE_URL}/students", json=student_data)
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    return response.json()


def test_generate_assignment_from_bob():
    """Test assignment generation from Bob IDE output"""
    print("\n=== Testing Assignment Generation from Bob IDE ===")
    
    # Simulated Bob IDE output (JSON format)
    bob_output = json.dumps({
        "title": "Python Loops - Beginner",
        "description": "Write a function that prints numbers from 1 to n using a for loop.",
        "test_cases": [
            {
                "input": "n = 5",
                "expected_output": "1\n2\n3\n4\n5",
                "description": "Print numbers 1 to 5"
            },
            {
                "input": "n = 3",
                "expected_output": "1\n2\n3",
                "description": "Print numbers 1 to 3"
            }
        ],
        "starter_code": "def print_numbers(n):\n    # Your code here\n    pass",
        "hints": [
            "Use a for loop with range()",
            "Remember that range(1, n+1) gives you 1 to n"
        ]
    })
    
    request_data = {
        "topic": "loops",
        "difficulty": "beginner",
        "bob_output": bob_output
    }
    
    response = requests.post(f"{BASE_URL}/api/assignments/generate", json=request_data)
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    return response.json()


def test_list_assignments():
    """Test listing assignments"""
    print("\n=== Listing All Assignments ===")
    response = requests.get(f"{BASE_URL}/assignments")
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    return response.json()


def test_submit_code(student_id, assignment_id):
    """Test code submission with validation"""
    print("\n=== Testing Code Submission ===")
    
    # Correct solution
    code = """
def print_numbers(n):
    for i in range(1, n + 1):
        print(i)

# Test
print_numbers(5)
"""
    
    submission_data = {
        "student_id": student_id,
        "assignment_id": assignment_id,
        "code": code
    }
    
    response = requests.post(f"{BASE_URL}/submissions", json=submission_data)
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    return response.json()


def test_submit_incorrect_code(student_id, assignment_id):
    """Test submission with incorrect code"""
    print("\n=== Testing Incorrect Code Submission ===")
    
    # Incorrect solution (off by one error)
    code = """
def print_numbers(n):
    for i in range(1, n):  # Missing +1
        print(i)

# Test
print_numbers(5)
"""
    
    submission_data = {
        "student_id": student_id,
        "assignment_id": assignment_id,
        "code": code
    }
    
    response = requests.post(f"{BASE_URL}/submissions", json=submission_data)
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    return response.json()


def test_list_submissions(student_id=None):
    """Test listing submissions"""
    print("\n=== Listing Submissions ===")
    url = f"{BASE_URL}/submissions"
    if student_id:
        url += f"?student_id={student_id}"
    
    response = requests.get(url)
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    return response.json()


def run_all_tests():
    """Run all Phase 2 tests"""
    print("=" * 60)
    print("PHASE 2 ASSIGNMENT SYSTEM TESTS")
    print("=" * 60)
    
    try:
        # Test 1: Health check
        if not test_health():
            print("\n❌ Health check failed!")
            return
        
        # Test 2: Create student
        student = test_create_student()
        student_id = student.get("id")
        
        # Test 3: Generate assignment from Bob output
        assignment = test_generate_assignment_from_bob()
        assignment_id = assignment.get("id")
        
        # Test 4: List assignments
        test_list_assignments()
        
        # Test 5: Submit correct code
        test_submit_code(student_id, assignment_id)
        
        # Test 6: Submit incorrect code
        test_submit_incorrect_code(student_id, assignment_id)
        
        # Test 7: List submissions
        test_list_submissions(student_id)
        
        print("\n" + "=" * 60)
        print("✅ ALL PHASE 2 TESTS COMPLETED!")
        print("=" * 60)
        
    except requests.exceptions.ConnectionError:
        print("\n❌ ERROR: Cannot connect to server. Make sure the backend is running on port 8000.")
    except Exception as e:
        print(f"\n❌ ERROR: {str(e)}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    run_all_tests()

# Made with Bob