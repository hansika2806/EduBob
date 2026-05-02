from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional


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


class AssignmentCreate(AssignmentBase):
    pass


class AssignmentResponse(AssignmentBase):
    id: int
    
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
    
    class Config:
        from_attributes = True


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
