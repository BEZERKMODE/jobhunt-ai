from sqlalchemy import Column, String, DateTime, Enum, Uuid
import uuid
from datetime import datetime
from .base import Base
import enum

class PlanEnum(str, enum.Enum):
    free = "free"
    pro = "pro"

class UserRole(str, enum.Enum):
    free_user = "free_user"
    pro_user = "pro_user"
    admin = "admin"

class User(Base):
    __tablename__ = "users"

    id = Column(Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(String, unique=True, index=True, nullable=False)
    name = Column(String, nullable=False)
    hashed_password = Column(String, nullable=False)
    role = Column(Enum(UserRole), default=UserRole.free_user, nullable=False)
    plan = Column(Enum(PlanEnum), default=PlanEnum.free, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
