from datetime import datetime
from typing import Optional
from decimal import Decimal

from bson import ObjectId
from fastapi import Form, UploadFile, File
from pydantic import BaseModel, Field


class SellPhotoResponse(BaseModel):
    id: str = Field(ObjectId, alias="_id")
    name: str
    url: str
    base_price: float
    sell_price: float
    description: str
    type: str
    status: str
    user_id: str
    buyer_id: Optional[str] = Field(ObjectId, alias="buyer_id")
    created_at: datetime
    updated_at: datetime
    deleted_at: Optional[datetime]

    class Config:
        from_attributes = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}

class CommentResponse(BaseModel):
    content: str
    user_id: str = Field(ObjectId, alias="user_id")

    class Config:
        from_attributes = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}

class PostPhotoResponse(BaseModel):
    id: str = Field(ObjectId, alias="_id")
    name: str
    url: str
    description: str
    type: str
    likes: int = 0
    comments: list[CommentResponse] = []
    liked: bool = False
    user_id: str
    created_at: datetime
    updated_at: datetime
    deleted_at: Optional[datetime]

    class Config:
        from_attributes = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}

class AddSellPhotoRequest(BaseModel):
    url: Optional[str] = None
    name: str
    base_price: float
    sell_price: float
    description: str
    file: Optional[UploadFile]
    user_id: Optional[str] = None

    @classmethod
    def as_form(
        cls,
        name: str = Form(...),
        base_price: float = Form(...),
        sell_price: float = Form(...),
        description: str = Form(...),
        url: Optional[str] = Form(None),
        user_id: Optional[str] = Form(None),
        file: UploadFile = File(...),
    ):
        return cls(name=name, base_price=base_price, description=description, url=url, user_id=user_id, file=file, sell_price=sell_price)

class AddPostPhotoRequest(BaseModel):
    url: Optional[str]
    name: str
    description: str
    user_id: Optional[str]
    file: Optional[UploadFile]

    @classmethod
    def as_form(
        cls,
        name: str = Form(...),
        description: str = Form(...),
        file: UploadFile = File(...),
        user_id: Optional[str] = Form(None),
        url: Optional[str] = Form(None),
    ):
        return cls(name=name, description=description, file=file, user_id=user_id, url=url)

class GetPhotoRequest(BaseModel):
    id: Optional[str]
    user_id: Optional[str]

class ListPhotoRequest(BaseModel):
    user_id: Optional[str] = Field(None, description="User ID")
    type: Optional[str] = None
    page: int = 1
    size: int = 10

class UpdateSellPhotoRequest(BaseModel):
    id: str
    name: Optional[str]
    base_price: Optional[Decimal]
    sell_price: Optional[Decimal]
    description: Optional[str]
    user_id: Optional[str]

class UpdatePostPhotoRequest(BaseModel):
    id: str
    name: Optional[str]
    description: Optional[str]
    user_id: Optional[str]

class DeletePhotoRequest(BaseModel):
    id: str
    user_id: str

class LikePhotoPostRequest(BaseModel):
    id: Optional[str] = None
    user_id: Optional[str] = None
    liked: bool