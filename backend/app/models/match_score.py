from sqlalchemy import Column, String, ForeignKey, DateTime, Float, Text
from sqlalchemy import Uuid, JSON
from datetime import datetime
from .base import Base
import uuid

class JobMatchScore(Base):
    __tablename__ = "job_match_scores"

    id = Column(Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(Uuid(as_uuid=True), ForeignKey("users.id"), nullable=False)
    job_id = Column(Uuid(as_uuid=True), ForeignKey("job_listings.id"), nullable=False)
    score = Column(Float, nullable=False)
    verdict = Column(Text)
    missing_skills = Column(JSON, default=[])
    created_at = Column(DateTime, default=datetime.utcnow)
