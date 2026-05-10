"""
EduBob API - Main application file with improved error handling,
database transaction management, security fixes, and comprehensive monitoring.
"""

from fastapi import FastAPI, Depends, HTTPException, status, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session, joinedload
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from typing import List, Optional
import uvicorn
import json
import logging
from datetime import datetime, timezone

from database import get_db, init_db
from models import Student, Assignment, Submission
from schemas import (
    StudentCreate, StudentResponse,
    AssignmentCreate, AssignmentResponse, AssignmentGenerateRequest,
    SubmissionCreate, SubmissionResponse, ValidationResult,
    ReviewRequest, ReviewResponse,
    CodebaseAnalyzeRequest, CodebaseAnalyzeResponse,
    ErrorResponse
)
from services.bob_client import generate_assignment, parse_test_cases
from services.validator import validate_submission, check_code_safety
from services.watsonx_client import analyze_class_patterns
from services.review_service import analyze_submission
from services.codebase_service import analyze_repo
from config import CORS_ORIGINS, DEFAULT_PAGE_SIZE, MAX_PAGE_SIZE

# Import middleware and utilities
from middleware.security_headers import SecurityHeadersMiddleware
from utils.logging_filter import setup_logging_with_filter
from utils.monitoring import get_comprehensive_health, get_system_metrics, check_database_health
from utils.backup import create_backup, list_backups, get_backup_info

# Configure logging with sensitive data filtering
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Setup logging filter
setup_logging_with_filter()

# Initialize FastAPI app
app = FastAPI(
    title="EduBob API",
    version="2.0.0",
    description="Educational platform with AI-powered code review, assignment generation, and comprehensive security",
    docs_url="/api/docs",
    redoc_url="/api/redoc",
    openapi_url="/api/openapi.json"
)

# Add security headers middleware
app.add_middleware(SecurityHeadersMiddleware)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def startup_event():
    """Initialize database and perform startup tasks"""
    try:
        init_db()
        logger.info("Database initialized successfully")
        
        # Create initial backup on startup
        backup_path = create_backup()
        if backup_path:
            logger.info(f"Startup backup created: {backup_path}")
        
        logger.info("Application startup complete")
    except Exception as e:
        logger.error(f"Failed to initialize application: {str(e)}")
        raise


@app.get("/health")
def health_check():
    """Basic health check endpoint"""
    return {
        "status": "OK",
        "timestamp": datetime.now(timezone.utc).isoformat()
    }


@app.get("/api/health/detailed")
def detailed_health_check():
    """
    Comprehensive health check endpoint.
    Returns detailed information about all subsystems.
    """
    try:
        health_data = get_comprehensive_health()
        
        # Determine overall status
        db_healthy = health_data["database"]["status"] == "healthy"
        overall_status = "healthy" if db_healthy else "degraded"
        health_data["status"] = overall_status
        
        return health_data
    except Exception as e:
        logger.error(f"Health check failed: {str(e)}")
        return JSONResponse(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            content={
                "status": "unhealthy",
                "error": str(e),
                "timestamp": datetime.now(timezone.utc).isoformat()
            }
        )


@app.get("/api/metrics")
def get_metrics():
    """
    Get system and application metrics.
    Useful for monitoring and alerting.
    """
    try:
        return {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "system": get_system_metrics(),
            "database": check_database_health()
        }
    except Exception as e:
        logger.error(f"Failed to get metrics: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to retrieve metrics: {str(e)}"
        )


@app.post("/api/admin/backup")
def create_database_backup():
    """
    Create a manual database backup.
    Returns the path to the created backup file.
    """
    try:
        backup_path = create_backup(compress=True)
        if backup_path:
            return {
                "success": True,
                "backup_path": backup_path,
                "timestamp": datetime.now(timezone.utc).isoformat()
            }
        else:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to create backup"
            )
    except Exception as e:
        logger.error(f"Backup creation failed: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Backup failed: {str(e)}"
        )


@app.get("/api/admin/backups")
def get_backups():
    """
    List all available database backups.
    """
    try:
        return get_backup_info()
    except Exception as e:
        logger.error(f"Failed to list backups: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to list backups: {str(e)}"
        )


# ==================== Student Endpoints ====================

@app.post(
    "/students",
    response_model=StudentResponse,
    status_code=status.HTTP_201_CREATED,
    responses={
        400: {"model": ErrorResponse, "description": "Email already registered"},
        500: {"model": ErrorResponse, "description": "Database error"}
    }
)
def create_student(student: StudentCreate, db: Session = Depends(get_db)):
    """
    Create a new student with proper transaction handling and race condition prevention.
    """
    try:
        # Create new student
        db_student = Student(
            name=student.name,
            email=student.email,
            role=student.role
        )
        db.add(db_student)
        db.commit()
        db.refresh(db_student)
        
        logger.info(f"Created student with ID: {db_student.id}")
        return db_student
        
    except IntegrityError as e:
        db.rollback()
        logger.warning(f"Duplicate email attempt: {student.email}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    except SQLAlchemyError as e:
        db.rollback()
        logger.error(f"Database error creating student: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Database error occurred"
        )
    except Exception as e:
        db.rollback()
        logger.error(f"Unexpected error creating student: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred"
        )


@app.get("/students", response_model=List[StudentResponse])
def list_students(
    skip: int = 0,
    limit: int = DEFAULT_PAGE_SIZE,
    db: Session = Depends(get_db)
):
    """List all students with pagination"""
    if limit > MAX_PAGE_SIZE:
        limit = MAX_PAGE_SIZE
    
    try:
        students = db.query(Student).offset(skip).limit(limit).all()
        return students
    except SQLAlchemyError as e:
        logger.error(f"Database error listing students: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Database error occurred"
        )


@app.get(
    "/students/{student_id}",
    response_model=StudentResponse,
    responses={404: {"model": ErrorResponse, "description": "Student not found"}}
)
def get_student(student_id: int, db: Session = Depends(get_db)):
    """Get a specific student by ID"""
    try:
        student = db.query(Student).filter(Student.id == student_id).first()
        if not student:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Student not found"
            )
        return student
    except HTTPException:
        raise
    except SQLAlchemyError as e:
        logger.error(f"Database error fetching student {student_id}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Database error occurred"
        )


# ==================== Assignment Endpoints ====================

@app.post(
    "/api/assignments/generate",
    response_model=AssignmentResponse,
    status_code=status.HTTP_201_CREATED,
    responses={400: {"model": ErrorResponse, "description": "Generation failed"}}
)
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
        
        # Create assignment in database with transaction handling
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
        
        logger.info(f"Generated assignment with ID: {db_assignment.id}")
        return db_assignment
        
    except SQLAlchemyError as e:
        db.rollback()
        logger.error(f"Database error generating assignment: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Database error occurred"
        )
    except Exception as e:
        db.rollback()
        logger.error(f"Failed to generate assignment: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Failed to generate assignment: {str(e)}"
        )


@app.post(
    "/assignments",
    response_model=AssignmentResponse,
    status_code=status.HTTP_201_CREATED
)
def create_assignment(assignment: AssignmentCreate, db: Session = Depends(get_db)):
    """Create a new assignment manually"""
    try:
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
        
        logger.info(f"Created assignment with ID: {db_assignment.id}")
        return db_assignment
        
    except SQLAlchemyError as e:
        db.rollback()
        logger.error(f"Database error creating assignment: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Database error occurred"
        )


@app.get("/assignments", response_model=List[AssignmentResponse])
def list_assignments(
    skip: int = 0,
    limit: int = DEFAULT_PAGE_SIZE,
    db: Session = Depends(get_db)
):
    """List all assignments with pagination"""
    if limit > MAX_PAGE_SIZE:
        limit = MAX_PAGE_SIZE
    
    try:
        assignments = db.query(Assignment).offset(skip).limit(limit).all()
        return assignments
    except SQLAlchemyError as e:
        logger.error(f"Database error listing assignments: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Database error occurred"
        )


@app.get(
    "/assignments/{assignment_id}",
    response_model=AssignmentResponse,
    responses={404: {"model": ErrorResponse, "description": "Assignment not found"}}
)
def get_assignment(assignment_id: int, db: Session = Depends(get_db)):
    """Get a specific assignment by ID"""
    try:
        assignment = db.query(Assignment).filter(Assignment.id == assignment_id).first()
        if not assignment:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Assignment not found"
            )
        return assignment
    except HTTPException:
        raise
    except SQLAlchemyError as e:
        logger.error(f"Database error fetching assignment {assignment_id}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Database error occurred"
        )


# ==================== Submission Endpoints ====================

@app.post(
    "/submissions",
    response_model=SubmissionResponse,
    status_code=status.HTTP_201_CREATED,
    responses={
        400: {"model": ErrorResponse, "description": "Validation failed"},
        404: {"model": ErrorResponse, "description": "Student or assignment not found"}
    }
)
def submit_code(submission: SubmissionCreate, db: Session = Depends(get_db)):
    """
    Submit code for an assignment and validate it.
    
    This endpoint:
    1. Checks code safety
    2. Validates against test cases
    3. Stores submission with results
    4. Generates AI review feedback (if provided)
    """
    try:
        # Verify student exists
        student = db.query(Student).filter(Student.id == submission.student_id).first()
        if not student:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Student not found"
            )
        
        # Verify assignment exists
        assignment = db.query(Assignment).filter(Assignment.id == submission.assignment_id).first()
        if not assignment:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Assignment not found"
            )
        
        # Check code safety
        safety_check = check_code_safety(submission.code)
        if not safety_check["safe"]:
            logger.warning(f"Unsafe code submission from student {submission.student_id}")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Code contains unsafe operations: {', '.join(safety_check['blocked_operations'])}"
            )
        
        # Parse test cases
        test_cases_json = assignment.test_cases if assignment.test_cases is not None else "[]"
        test_cases = parse_test_cases(str(test_cases_json))
        
        # Validate submission
        validation_result = validate_submission(submission.code, test_cases)
        
        # Generate AI review feedback if Bob output provided
        review_feedback = None
        if submission.bob_review_output:
            try:
                review_result = analyze_submission(
                    student_code=submission.code,
                    assignment_spec=str(assignment.description),
                    bob_output=submission.bob_review_output
                )
                review_feedback = json.dumps(review_result)
                logger.info(f"Generated review feedback for submission")
            except Exception as e:
                logger.error(f"Review generation failed: {str(e)}")
        
        # Create submission record
        db_submission = Submission(
            student_id=submission.student_id,
            assignment_id=submission.assignment_id,
            code=submission.code,
            status=validation_result["overall_status"],
            test_results=json.dumps(validation_result["test_results"]),
            passed_tests=validation_result["passed"],
            failed_tests=validation_result["failed"],
            total_tests=validation_result["total"],
            review_feedback=review_feedback
        )
        
        db.add(db_submission)
        db.commit()
        db.refresh(db_submission)
        
        logger.info(f"Created submission with ID: {db_submission.id}, status: {db_submission.status}")
        return db_submission
        
    except HTTPException:
        raise
    except SQLAlchemyError as e:
        db.rollback()
        logger.error(f"Database error creating submission: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Database error occurred"
        )
    except Exception as e:
        db.rollback()
        logger.error(f"Unexpected error creating submission: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred"
        )


@app.get("/submissions", response_model=List[SubmissionResponse])
def list_submissions(
    student_id: Optional[int] = None,
    assignment_id: Optional[int] = None,
    skip: int = 0,
    limit: int = DEFAULT_PAGE_SIZE,
    db: Session = Depends(get_db)
):
    """List submissions with optional filters and pagination"""
    if limit > MAX_PAGE_SIZE:
        limit = MAX_PAGE_SIZE
    
    try:
        query = db.query(Submission)
        
        if student_id:
            query = query.filter(Submission.student_id == student_id)
        if assignment_id:
            query = query.filter(Submission.assignment_id == assignment_id)
        
        submissions = query.offset(skip).limit(limit).all()
        return submissions
    except SQLAlchemyError as e:
        logger.error(f"Database error listing submissions: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Database error occurred"
        )


@app.get(
    "/submissions/{submission_id}",
    response_model=SubmissionResponse,
    responses={404: {"model": ErrorResponse, "description": "Submission not found"}}
)
def get_submission(submission_id: int, db: Session = Depends(get_db)):
    """Get a specific submission by ID"""
    try:
        submission = db.query(Submission).filter(Submission.id == submission_id).first()
        if not submission:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Submission not found"
            )
        return submission
    except HTTPException:
        raise
    except SQLAlchemyError as e:
        logger.error(f"Database error fetching submission {submission_id}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Database error occurred"
        )


# ==================== Phase 3: Code Review & Codebase Analysis ====================

@app.post(
    "/api/review/spec-check",
    response_model=ReviewResponse,
    responses={400: {"model": ErrorResponse, "description": "Review failed"}}
)
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
        
        logger.info("Code review completed successfully")
        return ReviewResponse(**review_result)
        
    except Exception as e:
        logger.error(f"Review failed: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Review failed: {str(e)}"
        )


@app.post(
    "/api/codebase/analyze",
    response_model=CodebaseAnalyzeResponse,
    responses={400: {"model": ErrorResponse, "description": "Analysis failed"}}
)
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
        
        logger.info(f"Codebase analysis completed for: {request.repo_url}")
        return CodebaseAnalyzeResponse(**analysis_result)
        
    except Exception as e:
        logger.error(f"Analysis failed: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Analysis failed: {str(e)}"
        )


@app.get(
    "/api/dashboard/class-stats",
    responses={500: {"model": ErrorResponse, "description": "Analysis failed"}}
)
def get_class_statistics(db: Session = Depends(get_db)):
    """
    Get class-wide statistics by analyzing student submission errors using watsonx.ai.
    
    This endpoint uses eager loading to prevent N+1 query problems.
    
    Returns:
        - total_submissions: Total number of submissions
        - common_errors: List of most common error patterns
        - struggling_concepts: List of concepts students struggle with
        - ai_reasoning: AI's reasoning for the analysis
        - analysis_method: Method used for analysis (watsonx or fallback)
    """
    try:
        # Fetch all submissions with eager loading to prevent N+1 queries
        submissions = db.query(Submission).options(
            joinedload(Submission.student),
            joinedload(Submission.assignment)
        ).all()
        
        # Extract error messages
        error_messages = []
        for submission in submissions:
            # Get error message if exists
            if submission.error_message is not None:
                error_msg = str(submission.error_message)
                if error_msg:
                    error_messages.append(error_msg)
            
            # Also extract errors from test results
            if submission.test_results is not None:
                test_results_str = str(submission.test_results)
                try:
                    test_results = json.loads(test_results_str)
                    for test in test_results:
                        if not test.get("passed") and test.get("error"):
                            error_messages.append(test["error"])
                except json.JSONDecodeError:
                    logger.warning(f"Failed to parse test results for submission {submission.id}")
                    pass
        
        # Analyze patterns using watsonx
        logger.info(f"Analyzing {len(error_messages)} error messages from {len(submissions)} submissions")
        analysis = analyze_class_patterns(error_messages)
        
        return {
            "total_submissions": len(submissions),
            "common_errors": analysis.get("common_errors", []),
            "struggling_concepts": analysis.get("struggling_concepts", []),
            "ai_reasoning": analysis.get("ai_reasoning", ""),
            "analysis_method": analysis.get("analysis_method", "")
        }
        
    except SQLAlchemyError as e:
        logger.error(f"Database error in class statistics: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Database error occurred"
        )
    except Exception as e:
        logger.error(f"Failed to analyze class stats: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to analyze class stats: {str(e)}"
        )


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)

# Made with Bob
