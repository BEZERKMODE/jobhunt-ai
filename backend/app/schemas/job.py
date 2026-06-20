from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
import uuid

class JobRead(BaseModel):
    id: uuid.UUID
    title: str
    company: str
    location: Optional[str] = None
    description: Optional[str] = None
    salary: Optional[float] = None
    posted_at: Optional[datetime] = None
    match_score: Optional[float] = None

    model_config = {"from_attributes": True}

class JobCreate(BaseModel):
    title: str = Field(..., max_length=200)
    company: str = Field(..., max_length=200)
    location: Optional[str] = None
    description: Optional[str] = None
    salary: Optional[float] = None
