"""
Demo Data Seeder for EduBob
Creates sample data for impressive hackathon demos
"""
import json
import sys
from datetime import datetime, timedelta
from database import SessionLocal, init_db
from models import Student, Assignment, Submission, Mistake

def seed_demo_data():
    """Seed database with demo data"""
    print("Seeding demo data...")
    
    # Initialize database
    init_db()
    db = SessionLocal()
    
    try:
        # Clear existing data (optional - comment out to preserve data)
        # db.query(Mistake).delete()
        # db.query(Submission).delete()
        # db.query(Assignment).delete()
        # db.query(Student).delete()
        
        # Create Students
        students = [
            Student(id=1, name="Alice Johnson", email="alice@example.com", role="student"),
            Student(id=2, name="Bob Smith", email="bob@example.com", role="student"),
            Student(id=3, name="Carol Davis", email="carol@example.com", role="student"),
            Student(id=4, name="David Wilson", email="david@example.com", role="student"),
            Student(id=5, name="Eve Martinez", email="eve@example.com", role="student"),
        ]
        
        for student in students:
            existing = db.query(Student).filter(Student.id == student.id).first()
            if not existing:
                db.add(student)
                print(f"[OK] Created student: {student.name}")
        
        db.commit()
        
        # Create Assignments
        assignments = [
            Assignment(
                id=1,
                title="Python Functions Basics",
                description="Learn to create and use functions in Python. Implement a function that calculates the factorial of a number.",
                test_cases=json.dumps([
                    {"name": "Test factorial(5)", "input": 5, "expected_output": 120},
                    {"name": "Test factorial(0)", "input": 0, "expected_output": 1},
                    {"name": "Test factorial(1)", "input": 1, "expected_output": 1}
                ]),
                starter_code="def factorial(n):\n    # Your code here\n    pass",
                hints=json.dumps(["Use recursion or iteration", "Handle base case n=0"]),
                topic="Functions",
                difficulty="beginner",
                created_at=datetime.utcnow() - timedelta(days=7)
            ),
            Assignment(
                id=2,
                title="List Manipulation",
                description="Work with Python lists. Create a function that removes duplicates from a list while preserving order.",
                test_cases=json.dumps([
                    {"name": "Test with duplicates", "input": [1,2,2,3,4,4,5], "expected_output": [1,2,3,4,5]},
                    {"name": "Test empty list", "input": [], "expected_output": []},
                    {"name": "Test no duplicates", "input": [1,2,3], "expected_output": [1,2,3]}
                ]),
                starter_code="def remove_duplicates(lst):\n    # Your code here\n    pass",
                hints=json.dumps(["Use a set to track seen elements", "Maintain insertion order"]),
                topic="Data Structures",
                difficulty="intermediate",
                created_at=datetime.utcnow() - timedelta(days=5)
            ),
            Assignment(
                id=3,
                title="String Reversal",
                description="Implement a function that reverses a string without using built-in reverse methods.",
                test_cases=json.dumps([
                    {"name": "Test normal string", "input": "hello", "expected_output": "olleh"},
                    {"name": "Test empty string", "input": "", "expected_output": ""},
                    {"name": "Test single char", "input": "a", "expected_output": "a"}
                ]),
                starter_code="def reverse_string(s):\n    # Your code here\n    pass",
                hints=json.dumps(["Use string slicing", "Or iterate backwards"]),
                topic="Strings",
                difficulty="beginner",
                created_at=datetime.utcnow() - timedelta(days=3)
            ),
        ]
        
        for assignment in assignments:
            existing = db.query(Assignment).filter(Assignment.id == assignment.id).first()
            if not existing:
                db.add(assignment)
                print(f"[OK] Created assignment: {assignment.title}")
        
        db.commit()
        
        # Create Submissions with varied results
        submissions_data = [
            # Alice - Good student
            {
                "student_id": 1, "assignment_id": 1, "status": "passed",
                "code": "def factorial(n):\n    if n == 0:\n        return 1\n    return n * factorial(n-1)",
                "passed_tests": 3, "failed_tests": 0, "total_tests": 3,
                "review_feedback": json.dumps({
                    "summary_feedback": "Excellent implementation! Clean recursive solution.",
                    "mistakes": [],
                    "improvement_suggestions": ["Consider adding input validation", "Could add iterative version for comparison"]
                })
            },
            {
                "student_id": 1, "assignment_id": 2, "status": "passed",
                "code": "def remove_duplicates(lst):\n    seen = set()\n    result = []\n    for item in lst:\n        if item not in seen:\n            seen.add(item)\n            result.append(item)\n    return result",
                "passed_tests": 3, "failed_tests": 0, "total_tests": 3,
                "review_feedback": json.dumps({
                    "summary_feedback": "Perfect solution with good use of set for tracking.",
                    "mistakes": [],
                    "improvement_suggestions": ["Could use dict.fromkeys() for a more Pythonic approach"]
                })
            },
            
            # Bob - Struggling student
            {
                "student_id": 2, "assignment_id": 1, "status": "failed",
                "code": "def factorial(n):\n    result = 1\n    for i in range(n):\n        result *= i\n    return result",
                "passed_tests": 0, "failed_tests": 3, "total_tests": 3,
                "error_message": "AssertionError: Expected 120, got 0",
                "review_feedback": json.dumps({
                    "summary_feedback": "Logic error in loop - starting from 0 causes multiplication by zero.",
                    "mistakes": [
                        "Loop starts at 0, should start at 1",
                        "Multiplying by 0 makes result always 0",
                        "Off-by-one error in range"
                    ],
                    "improvement_suggestions": [
                        "Use range(1, n+1) instead of range(n)",
                        "Test with simple inputs first",
                        "Add print statements to debug"
                    ]
                })
            },
            {
                "student_id": 2, "assignment_id": 1, "status": "partial",
                "code": "def factorial(n):\n    result = 1\n    for i in range(1, n):\n        result *= i\n    return result",
                "passed_tests": 1, "failed_tests": 2, "total_tests": 3,
                "error_message": "AssertionError: Expected 120, got 24",
                "review_feedback": json.dumps({
                    "summary_feedback": "Better! But still an off-by-one error.",
                    "mistakes": [
                        "Range should be range(1, n+1) not range(1, n)",
                        "Missing the last multiplication"
                    ],
                    "improvement_suggestions": [
                        "Remember range is exclusive of end value",
                        "Test with factorial(5) manually: 1*2*3*4*5"
                    ]
                })
            },
            
            # Carol - Average student
            {
                "student_id": 3, "assignment_id": 2, "status": "failed",
                "code": "def remove_duplicates(lst):\n    return list(set(lst))",
                "passed_tests": 1, "failed_tests": 2, "total_tests": 3,
                "error_message": "Order not preserved",
                "review_feedback": json.dumps({
                    "summary_feedback": "Removes duplicates but doesn't preserve order.",
                    "mistakes": [
                        "Using set() loses original order",
                        "Sets are unordered in Python"
                    ],
                    "improvement_suggestions": [
                        "Need to track order while removing duplicates",
                        "Use a list to maintain order and set to track seen items"
                    ]
                })
            },
            
            # David - Improving student
            {
                "student_id": 4, "assignment_id": 3, "status": "passed",
                "code": "def reverse_string(s):\n    return s[::-1]",
                "passed_tests": 3, "failed_tests": 0, "total_tests": 3,
                "review_feedback": json.dumps({
                    "summary_feedback": "Works perfectly! Very Pythonic solution.",
                    "mistakes": [],
                    "improvement_suggestions": [
                        "Try implementing without slicing for practice",
                        "Could use reversed() function as alternative"
                    ]
                })
            },
            
            # Eve - New student with common errors
            {
                "student_id": 5, "assignment_id": 1, "status": "failed",
                "code": "def factorial(n):\n    return n * factorial(n-1)",
                "passed_tests": 0, "failed_tests": 3, "total_tests": 3,
                "error_message": "RecursionError: maximum recursion depth exceeded",
                "review_feedback": json.dumps({
                    "summary_feedback": "Missing base case causes infinite recursion.",
                    "mistakes": [
                        "No base case to stop recursion",
                        "Will recurse infinitely until stack overflow",
                        "Need to handle n=0 or n=1"
                    ],
                    "improvement_suggestions": [
                        "Add: if n == 0: return 1",
                        "Always define base case first in recursive functions",
                        "Test with small inputs to verify base case works"
                    ]
                })
            },
        ]
        
        for i, sub_data in enumerate(submissions_data):
            submission = Submission(
                id=i+1,
                student_id=sub_data["student_id"],
                assignment_id=sub_data["assignment_id"],
                code=sub_data["code"],
                status=sub_data["status"],
                passed_tests=sub_data["passed_tests"],
                failed_tests=sub_data["failed_tests"],
                total_tests=sub_data["total_tests"],
                error_message=sub_data.get("error_message"),
                review_feedback=sub_data.get("review_feedback"),
                test_results=json.dumps([
                    {"name": f"Test {j+1}", "passed": j < sub_data["passed_tests"]}
                    for j in range(sub_data["total_tests"])
                ]),
                timestamp=datetime.utcnow() - timedelta(days=6-i, hours=i*2)
            )
            existing = db.query(Submission).filter(Submission.id == submission.id).first()
            if not existing:
                db.add(submission)
                print(f"[OK] Created submission {i+1}")
        
        db.commit()
        
        # Create Mistake Patterns
        mistakes = [
            Mistake(
                student_id=2,
                pattern=json.dumps({
                    "type": "off_by_one_error",
                    "description": "Frequently makes off-by-one errors in loops",
                    "examples": ["range(n) instead of range(n+1)", "Missing last iteration"]
                }),
                count=3,
                last_seen=datetime.utcnow() - timedelta(days=1)
            ),
            Mistake(
                student_id=5,
                pattern=json.dumps({
                    "type": "missing_base_case",
                    "description": "Forgets base cases in recursive functions",
                    "examples": ["Infinite recursion", "Stack overflow errors"]
                }),
                count=2,
                last_seen=datetime.utcnow()
            ),
            Mistake(
                student_id=3,
                pattern=json.dumps({
                    "type": "order_preservation",
                    "description": "Doesn't consider order preservation in data structures",
                    "examples": ["Using set() when order matters"]
                }),
                count=1,
                last_seen=datetime.utcnow() - timedelta(days=2)
            ),
        ]
        
        for mistake in mistakes:
            db.add(mistake)
            print(f"[OK] Created mistake pattern for student {mistake.student_id}")
        
        db.commit()
        
        print("\n[SUCCESS] Demo data seeded successfully!")
        print(f"   - {len(students)} students")
        print(f"   - {len(assignments)} assignments")
        print(f"   - {len(submissions_data)} submissions")
        print(f"   - {len(mistakes)} mistake patterns")
        print("\n[INFO] Ready for hackathon demo!")
        
    except Exception as e:
        print(f"[ERROR] Error seeding data: {str(e)}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    seed_demo_data()

# Made with Bob