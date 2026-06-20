from sqlalchemy import Column, String, ForeignKey, DateTime, Text
from sqlalchemy import Uuid
from datetime import datetime
from .base import Base
import uuid

class Application(Base):
    __tablename__ = "applications"

    id = Column(Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(Uuid(as_uuid=True), ForeignKey("users.id"), nullable=False)
    job_id = Column(Uuid(as_uuid=True), ForeignKey("job_listings.id"), nullable=False)
    status = Column(String, default="applied")
    applied_at = Column(DateTime, default=datetime.utcnow)
    platform = Column(String)
    cover_letter = Column(Text)
