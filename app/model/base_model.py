from datetime import datetime
from typing import Optional

from bson import ObjectId
from pydantic import Field, BaseModel

class Base(BaseModel):
    id: ObjectId = Field(default_factory=ObjectId, alias="_id")
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    deleted_at: Optional[datetime] = None

    class Config:
        from_attributes = True
        arbitrary_types_allowed = True