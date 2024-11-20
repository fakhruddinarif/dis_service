from datetime import datetime
from enum import Enum
from bson import ObjectId
from pydantic import Field, BaseModel

from app.model.base_model import Base
from typing import List, Optional


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
    id: str = Field(str, alias="_id") #payment["transaction_id"]
    status: PaymentStatus = PaymentStatus.PENDING
    type: str = "qris"
    url: str = None
    expired_at: Optional[str] = None

class Detail(BaseModel):
    seller_id: ObjectId
    photo_id: List[ObjectId]
    total: float

class Transaction(Base):
    buyer_id: ObjectId
    details: List[Detail]
    date: datetime = datetime.now()
    total: float = 0.0
    status: TransactionStatus = TransactionStatus.PENDING
    payment: Payment = None