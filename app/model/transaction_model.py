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

class Transaction(Base):
    buyer_id: ObjectId
    photo_id: List[ObjectId]
    date: datetime
    total: float = 0.0
    expired_at: datetime
    payment: Optional[dict] = None