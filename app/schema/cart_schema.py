from datetime import datetime
from typing import Optional

from bson import ObjectId
from pydantic import BaseModel, Field


class CartResponse(BaseModel):
    id: str = Field(ObjectId, alias="_id")
    photos: list[str]
    name_seller: str
    created_at: Optional[datetime]
    updated_at: Optional[datetime]
    deleted_at: Optional[datetime]

    class Config:
        from_attributes = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}

class ListCartResponse(BaseModel):
   url: str
   name_photo: str
   name_seller: str
   price: float

class AddItemRequest(BaseModel):
    photo_id: Optional[str] = None
    user_id: Optional[str] = None

class AddAllItemRequest(BaseModel):
    user_id: Optional[str] = None

class RemoveItemRequest(BaseModel):
    photo_id: Optional[str] = None
    user_id: Optional[str] = None

class RemoveAllItemRequest(BaseModel):
    user_id: Optional[str] = None

class ListItemRequest(BaseModel):
    user_id: Optional[str] = None
    page: int = 1
    size: int = 10