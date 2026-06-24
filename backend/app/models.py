from sqlalchemy import (
    Column, Integer, String, Float, Text, Boolean,
    DateTime, ForeignKey, Enum as SAEnum
)
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum

from app.db.session import Base


class ApplicationStatus(str, enum.Enum):
    pending = "pending"
    applied = "applied"
    rejected = "rejected"
    interview = "interview"
    offer = "offer"


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    full_name = Column(String(255))
    is_active = Column(Boolean, default=True)
    auto_apply_enabled = Column(Boolean, default=False)
    min_match_score = Column(Float, default=70.0)
    preferred_locations = Column(JSONB, default=list)
    preferred_roles = Column(JSONB, default=list)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    cvs = relationship("CV", back_populates="user", cascade="all, delete-orphan")
    applications = relationship("Application", back_populates="user", cascade="all, delete-orphan")


class CV(Base):
    __tablename__ = "cvs"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    filename = Column(String(255))
    text_content = Column(Text)  # extracted plain text
    file_data = Column(Text)     # base64 encoded original
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    user = relationship("User", back_populates="cvs")


class Job(Base):
    __tablename__ = "jobs"

    id = Column(Integer, primary_key=True, index=True)
    external_id = Column(String(500), unique=True, index=True)  # prevents duplicates
    title = Column(String(500), nullable=False)
    company = Column(String(255))
    location = Column(String(255))
    description = Column(Text)
    url = Column(String(2000))
    salary_min = Column(Float, nullable=True)
    salary_max = Column(Float, nullable=True)
    job_type = Column(String(100))  # full-time, contract, etc.
    source = Column(String(100), default="indeed")
    is_remote = Column(Boolean, default=False)
    posted_at = Column(DateTime(timezone=True), nullable=True)
    scraped_at = Column(DateTime(timezone=True), server_default=func.now())
    raw_data = Column(JSONB, default=dict)

    applications = relationship("Application", back_populates="job", cascade="all, delete-orphan")


class Application(Base):
    __tablename__ = "applications"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    job_id = Column(Integer, ForeignKey("jobs.id"), nullable=False)
    status = Column(
        SAEnum(ApplicationStatus),
        default=ApplicationStatus.pending,
        nullable=False
    )
    match_score = Column(Float, nullable=True)
    ai_analysis = Column(JSONB, nullable=True)   # full LLM response
    cover_letter = Column(Text, nullable=True)
    notes = Column(Text, nullable=True)
    applied_at = Column(DateTime(timezone=True), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    user = relationship("User", back_populates="applications")
    job = relationship("Job", back_populates="applications")
