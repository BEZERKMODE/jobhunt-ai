from sqlalchemy import Column, String, ForeignKey, Float
from sqlalchemy import Uuid, ARRAY, JSON
from .base import Base
import uuid

class CandidateProfile(Base):
    __tablename__ = "candidate_profiles"

    user_id = Column(Uuid(as_uuid=True), ForeignKey("users.id"), primary_key=True)
    summary = Column(String)
    skills = Column(JSON, default=[])
    experience = Column(JSON, default=[])  # Store array of experience objects
    education = Column(JSON, default=[])   # Store array of education objects
    languages = Column(JSON, default=[])
    
    # Extra fields
    phone = Column(String)
    location = Column(String)
    linkedin_url = Column(String)
    portfolio_url = Column(String)
