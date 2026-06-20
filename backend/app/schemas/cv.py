from pydantic import BaseModel
from typing import Optional
from datetime import datetime
import uuid

class CVRead(BaseModel):
    id: uuid.UUID
    user_id: uuid.UUID
    filename: str
    file_url: Optional[str] = None
    created_at: Optional[datetime] = None

    model_config = {"from_attributes": True}
