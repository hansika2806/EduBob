"""
Simple test script to verify the API endpoints work correctly.
Run this after starting the server with: python main.py
"""
import requests
import json

BASE_URL = "http://localhost:8000"

def test_health():
    """Test health check endpoint"""
    print("Testing GET /health...")
    response = requests.get(f"{BASE_URL}/health")
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    assert response.status_code == 200
    assert response.json()["status"] == "OK"
    print("[PASS] Health check passed\n")

def test_create_student():
    """Test creating a student"""
    print("Testing POST /students...")
    student_data = {
        "name": "John Doe",
        "email": "john@example.com",
        "role": "student"
    }
    response = requests.post(f"{BASE_URL}/students", json=student_data)
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    assert response.status_code == 201
    student = response.json()
    assert student["name"] == "John Doe"
    assert student["email"] == "john@example.com"
    print("[PASS] Student creation passed\n")
    return student["id"]

def test_list_students():
    """Test listing students"""
    print("Testing GET /students...")
    response = requests.get(f"{BASE_URL}/students")
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    assert response.status_code == 200
    students = response.json()
    assert len(students) > 0
    print("[PASS] List students passed\n")

def test_get_student(student_id):
    """Test getting a specific student"""
    print(f"Testing GET /students/{student_id}...")
    response = requests.get(f"{BASE_URL}/students/{student_id}")
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    assert response.status_code == 200
    student = response.json()
    assert student["id"] == student_id
    print("[PASS] Get student passed\n")

def test_duplicate_email():
    """Test that duplicate emails are rejected"""
    print("Testing duplicate email rejection...")
    student_data = {
        "name": "Jane Doe",
        "email": "john@example.com",  # Same email as before
        "role": "student"
    }
    response = requests.post(f"{BASE_URL}/students", json=student_data)
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    assert response.status_code == 400
    print("[PASS] Duplicate email rejection passed\n")

if __name__ == "__main__":
    print("=" * 50)
    print("EduBob API Tests - Phase 1")
    print("=" * 50 + "\n")
    
    try:
        test_health()
        student_id = test_create_student()
        test_list_students()
        test_get_student(student_id)
        test_duplicate_email()
        
        print("=" * 50)
        print("All tests passed! [SUCCESS]")
        print("=" * 50)
    except requests.exceptions.ConnectionError:
        print("ERROR: Could not connect to server.")
        print("Make sure the server is running: python main.py")
    except AssertionError as e:
        print(f"TEST FAILED: {e}")
    except Exception as e:
        print(f"ERROR: {e}")

# Made with Bob
