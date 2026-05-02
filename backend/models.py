from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime

Base = declarative_base()


class Student(Base):
    __tablename__ = "students"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, nullable=False, index=True)
    role = Column(String(20), default="student")
    
    # Relationships
    submissions = relationship("Submission", back_populates="student")
    mistakes = relationship("Mistake", back_populates="student")


class Assignment(Base):
    __tablename__ = "assignments"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False)
    description = Column(Text, nullable=False)
    test_cases = Column(Text, nullable=True)  # JSON string
    
    # Relationships
    submissions = relationship("Submission", back_populates="assignment")


class Submission(Base):
    __tablename__ = "submissions"
    
    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("students.id"), nullable=False)
    assignment_id = Column(Integer, ForeignKey("assignments.id"), nullable=False)
    code = Column(Text, nullable=False)
    status = Column(String(20), default="pending")  # pending, passed, failed
    timestamp = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    student = relationship("Student", back_populates="submissions")
    assignment = relationship("Assignment", back_populates="submissions")


class Mistake(Base):
    __tablename__ = "mistakes"
    
    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("students.id"), nullable=False)
    pattern = Column(Text, nullable=False)  # JSON string describing the mistake pattern
    count = Column(Integer, default=1)
    last_seen = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    student = relationship("Student", back_populates="mistakes")

# Made with Bob
