from datetime import datetime
from typing import Optional, List

from bson import ObjectId

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
    balance: float = 0.00
    followers: Optional[List[ObjectId]] = []
    following: Optional[List[ObjectId]] = []
    accounts: Optional[List[Account]] = []