from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional, List, Dict, Any


class StudentBase(BaseModel):
    name: str
    email: EmailStr
    role: str = "student"


class StudentCreate(StudentBase):
    pass


class StudentResponse(StudentBase):
    id: int
    
    class Config:
        from_attributes = True


class AssignmentBase(BaseModel):
    title: str
    description: str
    test_cases: Optional[str] = None
    starter_code: Optional[str] = None
    hints: Optional[str] = None
    topic: Optional[str] = None
    difficulty: Optional[str] = None


class AssignmentCreate(AssignmentBase):
    pass


class AssignmentGenerateRequest(BaseModel):
    """Request schema for generating assignment from Bob IDE output"""
    topic: str
    difficulty: str
    bob_output: str  # Raw output from Bob IDE session


class AssignmentResponse(AssignmentBase):
    id: int
    created_at: datetime
    
    class Config:
        from_attributes = True


class SubmissionBase(BaseModel):
    student_id: int
    assignment_id: int
    code: str


class SubmissionCreate(SubmissionBase):
    pass


class SubmissionResponse(SubmissionBase):
    id: int
    status: str
    timestamp: datetime
    test_results: Optional[str] = None
    passed_tests: int = 0
    failed_tests: int = 0
    total_tests: int = 0
    error_message: Optional[str] = None
    
    class Config:
        from_attributes = True


class ValidationResult(BaseModel):
    """Schema for code validation results"""
    passed: int
    failed: int
    total: int
    test_results: List[Dict[str, Any]]
    overall_status: str


class MistakeBase(BaseModel):
    student_id: int
    pattern: str


class MistakeCreate(MistakeBase):
    pass


class MistakeResponse(MistakeBase):
    id: int
    count: int
    last_seen: datetime
    
    class Config:
        from_attributes = True

# Made with Bob
