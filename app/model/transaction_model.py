from datetime import datetime
from enum import Enum
from bson import ObjectId
from pydantic import Field, BaseModel, validator
from typing import List, Optional
from app.model.base_model import Base

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

class Payment(BaseModel):
    id: str = Field(str, alias="_id")
    status: PaymentStatus = PaymentStatus.PENDING
    type: str = "qris"
    url: Optional[str] = None
    expired_at: Optional[str] = None

    class Config:
        from_attributes = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}

class Detail(BaseModel):
    seller_id: ObjectId
    photo_id: List[ObjectId]
    total: float

    class Config:
        from_attributes = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}

class Transaction(Base):
    buyer_id: ObjectId
    details: List[Detail]
    date: datetime = datetime.now()
    total: float = 0.0
    status: TransactionStatus = TransactionStatus.PENDING
    payment: Optional[Payment] = None

    @validator('buyer_id', pre=True, always=True)
    def validate_buyer_id(cls, v):
        return ObjectId(v) if isinstance(v, str) else v

    @validator('details', pre=True, each_item=True)
    def validate_details(cls, v):
        if isinstance(v, dict):
            v['seller_id'] = ObjectId(v['seller_id']) if isinstance(v['seller_id'], str) else v['seller_id']
            v['photo_id'] = [ObjectId(pid) if isinstance(pid, str) else pid for pid in v['photo_id']]
        return v