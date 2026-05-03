from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
import uvicorn
import json

from database import get_db, init_db
from models import Student, Assignment, Submission
from schemas import (
    StudentCreate, StudentResponse,
    AssignmentCreate, AssignmentResponse, AssignmentGenerateRequest,
    SubmissionCreate, SubmissionResponse, ValidationResult,
    ReviewRequest, ReviewResponse,
    CodebaseAnalyzeRequest, CodebaseAnalyzeResponse
)
from services.bob_client import generate_assignment, parse_test_cases
from services.validator import validate_submission, check_code_safety
from services.review_service import analyze_submission
from services.codebase_service import analyze_repo

# Initialize FastAPI app
app = FastAPI(title="EduBob API", version="1.0.0")


@app.on_event("startup")
def startup_event():
    """Initialize database on startup"""
    init_db()


@app.get("/health")
def health_check():
    """Health check endpoint"""
    return {"status": "OK"}


@app.post("/students", response_model=StudentResponse, status_code=201)
def create_student(student: StudentCreate, db: Session = Depends(get_db)):
    """Create a new student"""
    # Check if email already exists
    existing_student = db.query(Student).filter(Student.email == student.email).first()
    if existing_student:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    # Create new student
    db_student = Student(
        name=student.name,
        email=student.email,
        role=student.role
    )
    db.add(db_student)
    db.commit()
    db.refresh(db_student)
    return db_student


@app.get("/students", response_model=List[StudentResponse])
def list_students(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """List all students"""
    students = db.query(Student).offset(skip).limit(limit).all()
    return students


@app.get("/students/{student_id}", response_model=StudentResponse)
def get_student(student_id: int, db: Session = Depends(get_db)):
    """Get a specific student by ID"""
    student = db.query(Student).filter(Student.id == student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    return student


# ==================== Assignment Endpoints ====================

@app.post("/api/assignments/generate", response_model=AssignmentResponse, status_code=201)
def generate_assignment_from_bob(
    request: AssignmentGenerateRequest,
    db: Session = Depends(get_db)
):
    """
    Generate an assignment from Bob IDE output.
    
    This endpoint accepts Bob IDE output (pasted manually) and creates a structured assignment.
    """
    try:
        # Parse Bob IDE output using the bob_client service
        assignment_data = generate_assignment(
            bob_output=request.bob_output,
            topic=request.topic,
            difficulty=request.difficulty
        )
        
        # Create assignment in database
        db_assignment = Assignment(
            title=assignment_data["title"],
            description=assignment_data["description"],
            test_cases=json.dumps(assignment_data["test_cases"]),
            starter_code=assignment_data.get("starter_code"),
            hints=json.dumps(assignment_data.get("hints", [])),
            topic=assignment_data["topic"],
            difficulty=assignment_data["difficulty"]
        )
        
        db.add(db_assignment)
        db.commit()
        db.refresh(db_assignment)
        
        return db_assignment
        
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to generate assignment: {str(e)}")


@app.post("/assignments", response_model=AssignmentResponse, status_code=201)
def create_assignment(assignment: AssignmentCreate, db: Session = Depends(get_db)):
    """Create a new assignment manually"""
    db_assignment = Assignment(
        title=assignment.title,
        description=assignment.description,
        test_cases=assignment.test_cases,
        starter_code=assignment.starter_code,
        hints=assignment.hints,
        topic=assignment.topic,
        difficulty=assignment.difficulty
    )
    db.add(db_assignment)
    db.commit()
    db.refresh(db_assignment)
    return db_assignment


@app.get("/assignments", response_model=List[AssignmentResponse])
def list_assignments(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """List all assignments"""
    assignments = db.query(Assignment).offset(skip).limit(limit).all()
    return assignments


@app.get("/assignments/{assignment_id}", response_model=AssignmentResponse)
def get_assignment(assignment_id: int, db: Session = Depends(get_db)):
    """Get a specific assignment by ID"""
    assignment = db.query(Assignment).filter(Assignment.id == assignment_id).first()
    if not assignment:
        raise HTTPException(status_code=404, detail="Assignment not found")
    return assignment


# ==================== Submission Endpoints ====================

@app.post("/submissions", response_model=SubmissionResponse, status_code=201)
def submit_code(submission: SubmissionCreate, db: Session = Depends(get_db)):
    """
    Submit code for an assignment and validate it.
    
    This endpoint:
    1. Checks code safety
    2. Validates against test cases
    3. Stores submission with results
    """
    # Verify student exists
    student = db.query(Student).filter(Student.id == submission.student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    
    # Verify assignment exists
    assignment = db.query(Assignment).filter(Assignment.id == submission.assignment_id).first()
    if not assignment:
        raise HTTPException(status_code=404, detail="Assignment not found")
    
    # Check code safety
    safety_check = check_code_safety(submission.code)
    if not safety_check["safe"]:
        raise HTTPException(
            status_code=400,
            detail=f"Code contains unsafe operations: {', '.join(safety_check['blocked_operations'])}"
        )
    
    # Parse test cases - cast to str to satisfy type checker
    test_cases_json: str = assignment.test_cases or "[]"  # type: ignore
    test_cases = parse_test_cases(test_cases_json)
    
    # Validate submission
    validation_result = validate_submission(submission.code, test_cases)
    
    # Create submission record
    db_submission = Submission(
        student_id=submission.student_id,
        assignment_id=submission.assignment_id,
        code=submission.code,
        status=validation_result["overall_status"],
        test_results=json.dumps(validation_result["test_results"]),
        passed_tests=validation_result["passed"],
        failed_tests=validation_result["failed"],
        total_tests=validation_result["total"]
    )
    
    db.add(db_submission)
    db.commit()
    db.refresh(db_submission)
    
    return db_submission


@app.get("/submissions", response_model=List[SubmissionResponse])
def list_submissions(
    student_id: Optional[int] = None,
    assignment_id: Optional[int] = None,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """List submissions with optional filters"""
    query = db.query(Submission)
    
    if student_id:
        query = query.filter(Submission.student_id == student_id)
    if assignment_id:
        query = query.filter(Submission.assignment_id == assignment_id)
    
    submissions = query.offset(skip).limit(limit).all()
    return submissions


@app.get("/submissions/{submission_id}", response_model=SubmissionResponse)
def get_submission(submission_id: int, db: Session = Depends(get_db)):
    """Get a specific submission by ID"""
    submission = db.query(Submission).filter(Submission.id == submission_id).first()
    if not submission:
        raise HTTPException(status_code=404, detail="Submission not found")
    return submission


# ==================== Phase 3: Code Review & Codebase Analysis ====================

@app.post("/api/review/spec-check", response_model=ReviewResponse)
def review_submission(request: ReviewRequest):
    """
    Review student code against assignment specification.
    
    This endpoint accepts Bob IDE output (pasted manually from Ask mode session)
    and provides structured feedback on the student's submission.
    
    Note: Bob IDE output is passed here from manual Ask mode session.
    This does NOT call Bob via subprocess or CLI.
    """
    try:
        # Analyze submission using Bob IDE output
        review_result = analyze_submission(
            student_code=request.student_code,
            assignment_spec=request.assignment_spec,
            bob_output=request.bob_output
        )
        
        return ReviewResponse(**review_result)
        
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Review failed: {str(e)}")


@app.post("/api/codebase/analyze", response_model=CodebaseAnalyzeResponse)
def analyze_codebase(request: CodebaseAnalyzeRequest):
    """
    Analyze repository structure and architecture.
    
    This endpoint accepts Bob IDE output (pasted manually from Ask mode session)
    containing full codebase analysis.
    
    Note:
    - repo_url is stored for reference only (repository is NOT cloned)
    - Bob IDE output contains the full analysis from manual session
    - This does NOT install gitpython or clone repositories
    """
    try:
        # Analyze codebase using Bob IDE output
        analysis_result = analyze_repo(
            repo_url=request.repo_url,
            bob_output=request.bob_output
        )
        
        return CodebaseAnalyzeResponse(**analysis_result)
        
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Analysis failed: {str(e)}")


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)

# Made with Bob
