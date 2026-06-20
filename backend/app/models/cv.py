from sqlalchemy import Column, String, ForeignKey, DateTime, Boolean, Integer
from sqlalchemy import Uuid
from datetime import datetime
from .base import Base
import uuid

class CVFile(Base):
    __tablename__ = "cv_files"

    id = Column(Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(Uuid(as_uuid=True), ForeignKey("users.id"), nullable=False)
    filename = Column(String, nullable=False, server_default='')
    file_url = Column(String, nullable=False)
    version = Column(Integer, default=1)
    parsed_at = Column(DateTime)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
