from datetime import datetime
from typing import Optional, List
from decimal import Decimal
from pydantic import Field
from bson import Decimal128
from app.model.base_model import Base

class Account(Base):
    bank: str
    name: str
    number: str

class User(Base):
    name: str
    phone: str
    email: str
    password: str
    username: Optional[str] = None
    photo: Optional[str] = None
    role: str = "user"
    email_verified_at: Optional[datetime] = None
    balance: Decimal128 = Field(default_factory=lambda: Decimal128(Decimal("0.00")))
    accounts: Optional[List[Account]] = []