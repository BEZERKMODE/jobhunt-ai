from pydantic import BaseModel, Field
from typing import Optional
from enum import Enum
from datetime import datetime
import uuid

class ApplicationStatus(str, Enum):
    PENDING = 'PENDING'
    APPLIED = 'APPLIED'
    INTERVIEW = 'INTERVIEW'
    REJECTED = 'REJECTED'
    OFFERED = 'OFFERED'

class ApplicationRead(BaseModel):
    id: uuid.UUID
    job_id: uuid.UUID
    user_id: uuid.UUID
    status: ApplicationStatus
    applied_at: Optional[datetime] = None

    model_config = {"from_attributes": True}

class ApplicationCreate(BaseModel):
    job_id: str
