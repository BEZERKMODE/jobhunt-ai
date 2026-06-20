from sqlalchemy import Column, String, DateTime, Text, JSON, Integer, Boolean
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime
from .base import Base
import uuid

class JobListing(Base):
    __tablename__ = "job_listings"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = Column(String, nullable=False, index=True)
    company = Column(String, nullable=False, index=True)
    location = Column(String)
    salary_min = Column(Integer, nullable=True)
    salary_max = Column(Integer, nullable=True)
    is_remote = Column(Boolean, default=False)
    experience_level = Column(String, nullable=True)  # junior, mid, senior

    posted_at = Column(DateTime)
    description = Column(Text)
    url = Column(String, unique=True)
    raw_data = Column(JSON) # Store raw JSON from external APIs
    created_at = Column(DateTime, default=datetime.utcnow)
