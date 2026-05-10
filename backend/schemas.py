"""
Pydantic schemas for request/response validation.
Includes input length validation and centralized JSON parsing.
"""

from pydantic import BaseModel, EmailStr, field_validator, Field
from datetime import datetime
from typing import Optional, List, Dict, Any
import json

from config import (
    MAX_CODE_LENGTH,
    MAX_PROMPT_LENGTH,
    MAX_ASSIGNMENT_TITLE_LENGTH,
    MAX_ASSIGNMENT_DESCRIPTION_LENGTH
)


def parse_json_field(v: Any, default: Any = None) -> Any:
    """
    Centralized JSON parsing utility to eliminate DRY violations.
    
    Args:
        v: Value to parse (can be string or already parsed)
        default: Default value if parsing fails
    
    Returns:
        Parsed value or default
    """
    if isinstance(v, str):
        try:
            return json.loads(v)
        except json.JSONDecodeError:
            return default if default is not None else []
    return v


class StudentBase(BaseModel):
    """Base schema for student data"""
    name: str = Field(..., min_length=1, max_length=200)
    email: EmailStr
    role: str = Field(default="student", pattern="^(student|teacher)$")


class StudentCreate(StudentBase):
    """Schema for creating a new student"""
    pass


class StudentResponse(StudentBase):
    """Schema for student response"""
    id: int
    
    class Config:
        from_attributes = True


class AssignmentBase(BaseModel):
    """Base schema for assignment data"""
    title: str = Field(..., min_length=1, max_length=MAX_ASSIGNMENT_TITLE_LENGTH)
    description: str = Field(..., min_length=1, max_length=MAX_ASSIGNMENT_DESCRIPTION_LENGTH)
    test_cases: Optional[List[Dict[str, Any]]] = None
    starter_code: Optional[str] = Field(None, max_length=MAX_CODE_LENGTH)
    hints: Optional[List[str]] = None
    topic: Optional[str] = Field(None, max_length=100)
    difficulty: Optional[str] = Field(None, pattern="^(easy|medium|hard|beginner|intermediate|advanced)$")


class AssignmentCreate(AssignmentBase):
    """Schema for creating a new assignment"""
    pass


class AssignmentGenerateRequest(BaseModel):
    """Request schema for generating assignment from Bob IDE output"""
    topic: str = Field(..., min_length=1, max_length=200)
    difficulty: str = Field(..., pattern="^(easy|medium|hard|beginner|intermediate|advanced)$")
    bob_output: str = Field(..., min_length=1, max_length=MAX_PROMPT_LENGTH)


class AssignmentResponse(AssignmentBase):
    """Schema for assignment response"""
    id: int
    created_at: datetime
    
    @field_validator('test_cases', mode='before')
    @classmethod
    def parse_test_cases(cls, v):
        """Parse test_cases from JSON string if needed"""
        return parse_json_field(v, default=[])
    
    @field_validator('hints', mode='before')
    @classmethod
    def parse_hints(cls, v):
        """Parse hints from JSON string if needed"""
        return parse_json_field(v, default=[])
    
    class Config:
        from_attributes = True


class SubmissionBase(BaseModel):
    """Base schema for submission data"""
    student_id: int = Field(..., gt=0)
    assignment_id: int = Field(..., gt=0)
    code: str = Field(..., min_length=1, max_length=MAX_CODE_LENGTH)


class SubmissionCreate(SubmissionBase):
    """Schema for creating a new submission"""
    bob_review_output: Optional[str] = Field(None, max_length=MAX_PROMPT_LENGTH)


class SubmissionResponse(SubmissionBase):
    """Schema for submission response"""
    id: int
    status: str
    timestamp: datetime
    test_results: Optional[List[Dict[str, Any]]] = None
    passed_tests: int = 0
    failed_tests: int = 0
    total_tests: int = 0
    error_message: Optional[str] = None
    review_feedback: Optional[Dict[str, Any]] = None
    
    @field_validator('test_results', mode='before')
    @classmethod
    def parse_test_results(cls, v):
        """Parse test_results from JSON string if needed"""
        return parse_json_field(v, default=[])
    
    @field_validator('review_feedback', mode='before')
    @classmethod
    def parse_review_feedback(cls, v):
        """Parse review_feedback from JSON string if needed"""
        return parse_json_field(v, default=None)
    
    class Config:
        from_attributes = True


class ValidationResult(BaseModel):
    """Schema for code validation results"""
    passed: int = Field(..., ge=0)
    failed: int = Field(..., ge=0)
    total: int = Field(..., ge=0)
    test_results: List[Dict[str, Any]]
    overall_status: str = Field(..., pattern="^(passed|partial|failed|error)$")


class MistakeBase(BaseModel):
    """Base schema for mistake tracking"""
    student_id: int = Field(..., gt=0)
    pattern: str = Field(..., min_length=1, max_length=500)


class MistakeCreate(MistakeBase):
    """Schema for creating a mistake record"""
    pass


class MistakeResponse(MistakeBase):
    """Schema for mistake response"""
    id: int
    count: int = Field(..., ge=0)
    last_seen: datetime
    
    class Config:
        from_attributes = True


# ==================== Phase 3: Code Review Schemas ====================

class ReviewRequest(BaseModel):
    """Request schema for code review"""
    student_code: str = Field(..., min_length=1, max_length=MAX_CODE_LENGTH)
    assignment_spec: str = Field(..., min_length=1, max_length=MAX_ASSIGNMENT_DESCRIPTION_LENGTH)
    bob_output: str = Field(..., min_length=1, max_length=MAX_PROMPT_LENGTH)


class ReviewResponse(BaseModel):
    """Response schema for code review"""
    summary_feedback: str
    mistakes: List[str]
    improvement_suggestions: List[str]


class CodebaseAnalyzeRequest(BaseModel):
    """Request schema for codebase analysis"""
    repo_url: str = Field(..., min_length=1, max_length=500)
    bob_output: str = Field(..., min_length=1, max_length=MAX_PROMPT_LENGTH)


class CodebaseAnalyzeResponse(BaseModel):
    """Response schema for codebase analysis"""
    architecture_summary: str
    key_files: List[Dict[str, str]]
    tech_stack: List[str]
    explanation: str


class ErrorResponse(BaseModel):
    """
    Standard error response schema.
    Used for documenting error responses across all endpoints.
    """
    detail: str = Field(..., description="Error message describing what went wrong")
    error_code: Optional[str] = Field(None, description="Machine-readable error code")
    timestamp: datetime = Field(default_factory=datetime.utcnow, description="When the error occurred")
    
    class Config:
        json_schema_extra = {
            "example": {
                "detail": "Invalid input: code exceeds maximum length",
                "error_code": "VALIDATION_ERROR",
                "timestamp": "2024-01-01T12:00:00Z"
            }
        }


# Made with Bob
