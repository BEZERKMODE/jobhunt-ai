from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime
import uuid

class ProfileRead(BaseModel):
    id: uuid.UUID
    name: str
    email: EmailStr
    role: Optional[str] = None
    plan: Optional[str] = None
    created_at: Optional[datetime] = None

    model_config = {"from_attributes": True}

class ProfileUpdate(BaseModel):
    name: Optional[str] = Field(None, max_length=100)
    email: Optional[EmailStr] = None
    # add any other updatable fields here
