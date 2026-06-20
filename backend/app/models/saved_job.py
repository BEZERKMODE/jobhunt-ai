from sqlalchemy import Column, String, ForeignKey, DateTime, Text
from sqlalchemy import Uuid
from datetime import datetime
from .base import Base
import uuid

class SavedJob(Base):
    __tablename__ = "saved_jobs"

    id = Column(Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(Uuid(as_uuid=True), ForeignKey("users.id"), nullable=False)
    job_id = Column(Uuid(as_uuid=True), ForeignKey("job_listings.id"), nullable=False)
    note = Column(Text)
    reminder_date = Column(DateTime)
    collection_name = Column(String, default="default")
    saved_at = Column(DateTime, default=datetime.utcnow)
