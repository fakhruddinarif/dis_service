from datetime import datetime
from typing import Optional, List
from enum import Enum
from bson import ObjectId
from pydantic import BaseModel, Field

class TransactionStatus(str, Enum):
    PENDING = "pending"
    PAID = "paid"
    EXPIRED = "expired"
    CANCELLED = "cancelled"

class PaymentStatus(str, Enum):
    PENDING = "pending"
    CANCEL = "cancel"
    SETTLEMENT = "settlement"
    EXPIRE = "expire"
    DENY = "deny"

class PaymentResponse(BaseModel):
    id: str = Field(str, alias="_id")
    status: PaymentStatus = PaymentStatus.PENDING
    type: str = "qris"
    url: str = None
    expired_at: Optional[str] = None

class DetailResponse(BaseModel):
    seller_id: str = Field(ObjectId, alias="seller_id")
    photo_id: List[str] = Field(List[ObjectId], alias="photo_id")
    total: float

class TransactionResponse(BaseModel):
    id: str = Field(ObjectId, alias="_id")
    buyer_id: str = Field(ObjectId, alias="buyer_id")
    details: List[DetailResponse]
    date: Optional[datetime]
    total: float
    status: TransactionStatus = TransactionStatus.PENDING
    payment: PaymentResponse = None
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
    qris: dict

class GetTransactionRequest(BaseModel):
    user_id: Optional[str] = None
    id: Optional[str] = None

class ListTransactionRequest(BaseModel):
    user_id: Optional[str] = None
    page: int = 1
    size: int = 10