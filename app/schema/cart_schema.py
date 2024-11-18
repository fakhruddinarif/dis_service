from datetime import datetime
from typing import Optional

from bson import ObjectId
from pydantic import BaseModel, Field


class CartResponse(BaseModel):
    id: str = Field(ObjectId, alias="_id")
    photos: list[str]
    user_id: str
    created_at: Optional[datetime]
    updated_at: Optional[datetime]
    deleted_at: Optional[datetime]

    class Config:
        from_attributes = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}

class AddItemRequest(BaseModel):
    photo_id: str
    user_id: str

class RemoveItemRequest(BaseModel):
    photo_id: str
    user_id: str

class ListItemRequest(BaseModel):
    user_id: str
    page: int = 1
    size: int = 10