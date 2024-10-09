from datetime import datetime
from typing import Optional
from decimal import Decimal
from bson import Decimal128
from fastapi import UploadFile
from pydantic import BaseModel


class PhotoResponse(BaseModel):
    _id: str
    name: str
    url: str
    base_price: Decimal128(Decimal("0.00"))
    sell_price: Decimal128(Decimal("0.00"))
    description: str
    user_id: str
    created_at: datetime
    updated_at: datetime
    deleted_at: Optional[datetime]

    class Config:
        from_attributes = True
        arbitrary_types_allowed = True

class AddPhotoRequest(BaseModel):
    photo: UploadFile
    name: str
    base_price: Decimal
    sell_price: Decimal
    description: str
    user_id: str

class GetPhotoRequest(BaseModel):
    id: str
    user_id: str

class ListPhotoRequest(BaseModel):
    user_id: str
    page: int
    per_page: int

class UpdatePhotoRequest(BaseModel):
    id: str
    name: Optional[str]
    base_price: Optional[Decimal]
    sell_price: Optional[Decimal]
    description: Optional[str]

class DeletePhotoRequest(BaseModel):
    id: str
    user_id: str