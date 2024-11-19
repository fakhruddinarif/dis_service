from datetime import datetime
from typing import Optional, List

from bson import ObjectId
from pydantic import BaseModel, Field

class TransactionResponse(BaseModel):
    id: str = Field(ObjectId, alias="_id")
    buyer_id: str = Field(ObjectId, alias="buyer_id")
    photo_id: List[str] = Field(List[ObjectId], alias="photo_id")
    date: Optional[datetime]
    total: float
    expired_at: Optional[datetime]
    payment: Optional[dict] = None
    created_at: Optional[datetime]
    updated_at: Optional[datetime]
    deleted_at: Optional[datetime]

    class Config:
        from_attributes = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}

class TransactionRequest(BaseModel):
    buyer_id: Optional[str] = Field(None, alias="buyer_id")
    photo_id: List[str] = Field(List[None], alias="photo_id")
    total: Optional[float] = None

class TransactionDetailMidtransRequest(BaseModel):
    order_id: str
    gross_amount: int

class PaymentMidtransRequest(BaseModel):
    payment_type: str = "qris"
    transaction_details: TransactionDetailMidtransRequest
