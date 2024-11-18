from datetime import datetime
from typing import Optional, List

from bson import ObjectId
from pydantic import BaseModel, Field

class TransactionResponse(BaseModel):
    id: str = Field(ObjectId, alias="_id")
    buyer_id: str = Field(ObjectId, alias="buyer_id")
    photo_id: List[str] = Field(List[ObjectId], alias="photo_id")
    date: datetime
    total: float
    payment: dict
    created_at: Optional[datetime]
    updated_at: Optional[datetime]
    deleted_at: Optional[datetime]

    class Config:
        from_attributes = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}

class PaymentRequest(BaseModel):
    url: str
    type: str = "qris"
    status: str
    midtrans_payment: dict
    expired_at: datetime

class TransactionRequest(BaseModel):
    buyer_id: Optional[str] = Field(None, alias="buyer_id")
    photo_id: List[str] = Field(List[None], alias="photo_id")
    total: float