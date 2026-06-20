from sqlalchemy import Column, String, ForeignKey, DateTime
from sqlalchemy import Uuid
from datetime import datetime
from .base import Base
import uuid

class Subscription(Base):
    __tablename__ = "subscriptions"

    id = Column(Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(Uuid(as_uuid=True), ForeignKey("users.id"), nullable=False)
    plan = Column(String, nullable=False)
    stripe_customer_id = Column(String)
    status = Column(String, nullable=False)
    expires_at = Column(DateTime)
    created_at = Column(DateTime, default=datetime.utcnow)
