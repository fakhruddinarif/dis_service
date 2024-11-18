from datetime import datetime
from enum import Enum
from bson import ObjectId
from app.model.base_model import Base
from typing import List, Optional


class PaymentStatus(str, Enum):
    PENDING = "pending"
    PAID = "paid"
    EXPIRED = "expired"
    FAILED = "failed"
    SUCCESS = "success"

class MidtransPayment(Base):
    response: dict

class Payment:
    url: str
    type: str = "qris"
    status: PaymentStatus
    midtrans_payment: MidtransPayment
    expired_at: datetime

class Transaction(Base):
    buyer_id: ObjectId
    photo_id: List[ObjectId]
    date: datetime = datetime.now()
    total: float
    payment: Optional[Payment]
