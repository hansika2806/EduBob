from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
import uvicorn

from database import get_db, init_db
from models import Student
from schemas import StudentCreate, StudentResponse

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


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)

# Made with Bob
