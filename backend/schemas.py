from pydantic import BaseModel, EmailStr, field_validator
from datetime import datetime
from typing import Optional, List, Dict, Any
import json


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
    test_cases: Optional[List[Dict[str, Any]]] = None
    starter_code: Optional[str] = None
    hints: Optional[List[str]] = None
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
    
    @field_validator('test_cases', mode='before')
    @classmethod
    def parse_test_cases(cls, v):
        if isinstance(v, str):
            try:
                return json.loads(v)
            except json.JSONDecodeError:
                return []
        return v
    
    @field_validator('hints', mode='before')
    @classmethod
    def parse_hints(cls, v):
        if isinstance(v, str):
            try:
                return json.loads(v)
            except json.JSONDecodeError:
                return []
        return v
    
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
    test_results: Optional[List[Dict[str, Any]]] = None
    passed_tests: int = 0
    failed_tests: int = 0
    total_tests: int = 0
    error_message: Optional[str] = None
    
    @field_validator('test_results', mode='before')
    @classmethod
    def parse_test_results(cls, v):
        if isinstance(v, str):
            try:
                return json.loads(v)
            except json.JSONDecodeError:
                return []
        return v
    
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


# ==================== Phase 3: Code Review Schemas ====================

class ReviewRequest(BaseModel):
    """Request schema for code review"""
    student_code: str
    assignment_spec: str
    bob_output: str  # Bob IDE output from manual Ask mode session


class ReviewResponse(BaseModel):
    """Response schema for code review"""
    summary_feedback: str
    mistakes: List[str]
    improvement_suggestions: List[str]


class CodebaseAnalyzeRequest(BaseModel):
    """Request schema for codebase analysis"""
    repo_url: str  # Repository URL (stored for reference only)
    bob_output: str  # Bob IDE output contains full analysis


class CodebaseAnalyzeResponse(BaseModel):
    """Response schema for codebase analysis"""
    architecture_summary: str
    key_files: List[Dict[str, str]]
    tech_stack: List[str]
    explanation: str


# Made with Bob
