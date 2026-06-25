from pydantic import BaseModel, EmailStr, field_validator
from typing import Optional, List, Any
from datetime import datetime
from enum import Enum


# ─── Auth ────────────────────────────────────────────────────────────────────

class UserRegister(BaseModel):
    email: EmailStr
    password: str
    full_name: Optional[str] = None

    @field_validator("password")
    @classmethod
    def password_strength(cls, v):
        if len(v) < 8:
            raise ValueError("Password must be at least 8 characters")
        return v


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


class UserOut(BaseModel):
    id: int
    email: str
    full_name: Optional[str]
    is_active: bool
    auto_apply_enabled: bool
    min_match_score: float
    preferred_locations: List[str] = []
    preferred_roles: List[str] = []
    created_at: datetime

    class Config:
        from_attributes = True


# ─── Profile ─────────────────────────────────────────────────────────────────

class ProfileUpdate(BaseModel):
    full_name: Optional[str] = None
    auto_apply_enabled: Optional[bool] = None
    min_match_score: Optional[float] = None
    preferred_locations: Optional[List[str]] = None
    preferred_roles: Optional[List[str]] = None


# ─── CV ──────────────────────────────────────────────────────────────────────

class CVOut(BaseModel):
    id: int
    filename: Optional[str]
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True


# ─── Jobs ────────────────────────────────────────────────────────────────────

class JobOut(BaseModel):
    id: int
    title: str
    company: Optional[str]
    location: Optional[str]
    description: Optional[str]
    url: Optional[str]
    salary_min: Optional[float]
    salary_max: Optional[float]
    job_type: Optional[str]
    source: str
    is_remote: bool
    scraped_at: datetime
    match_score: Optional[float] = None  # injected from Application when queried

    class Config:
        from_attributes = True


class JobCreate(BaseModel):
    external_id: str
    title: str
    company: Optional[str] = None
    location: Optional[str] = None
    description: Optional[str] = None
    url: Optional[str] = None
    salary_min: Optional[float] = None
    salary_max: Optional[float] = None
    job_type: Optional[str] = None
    source: str = "indeed"
    is_remote: bool = False
    raw_data: dict = {}


# ─── Applications ────────────────────────────────────────────────────────────

class ApplicationStatus(str, Enum):
    pending = "pending"
    applied = "applied"
    rejected = "rejected"
    interview = "interview"
    offer = "offer"


class ApplicationCreate(BaseModel):
    job_id: int
    cover_letter: Optional[str] = None
    notes: Optional[str] = None


class ApplicationOut(BaseModel):
    id: int
    job_id: int
    status: str
    match_score: Optional[float]
    cover_letter: Optional[str]
    notes: Optional[str]
    ai_analysis: Optional[Any]
    applied_at: Optional[datetime]
    created_at: datetime
    job: JobOut

    class Config:
        from_attributes = True


class ApplicationUpdate(BaseModel):
    status: Optional[ApplicationStatus] = None
    notes: Optional[str] = None


# ─── Tasks / Scraping ────────────────────────────────────────────────────────

class ScrapeRequest(BaseModel):
    query: str
    location: str = "remote"
    source: str = "indeed"
    max_results: int = 20


class TaskResponse(BaseModel):
    task_id: str
    status: str
    message: str


# ─── Insights ────────────────────────────────────────────────────────────────

class ScoreDistribution(BaseModel):
    range_0_40: int
    range_41_60: int
    range_61_80: int
    range_81_100: int


class TopJob(BaseModel):
    title: str
    company: Optional[str]
    score: Optional[float]
    job_id: int


class DashboardInsights(BaseModel):
    total_jobs_scraped: int
    total_applications: int
    applications_sent: int
    avg_match_score: float
    score_distribution: ScoreDistribution
    top_matched_jobs: List[TopJob]
    status_breakdown: dict
    recent_activity: List[dict]
