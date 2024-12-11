from typing import Optional
from enum import Enum

from bson import ObjectId

from app.model.base_model import Base

class WithdrawalStatus(str, Enum):
    PENDING = "pending"
    SUCCESS = "success"
    FAILED = "failed"

class Withdrawal(Base):
    user_id: ObjectId
    account_id: ObjectId
    amount: float = 0.00
    status: WithdrawalStatus = WithdrawalStatus.PENDING
    receipt: Optional[str] = None
    note: Optional[str] = None