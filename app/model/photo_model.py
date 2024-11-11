from typing import Optional, List

from bson import ObjectId, Decimal128
from decimal import Decimal

from pydantic import Field

from app.model.base_model import Base

class SellPhoto(Base):
    url: str
    name: str
    base_price: float = 0.00
    sell_price: float = 0.00
    type: str = "sell"
    is_sold: bool = False
    description: str
    user_id: ObjectId
    buyer_id: Optional[ObjectId] = Field(None, alias="buyer_id")

class Comment(Base):
    content: str
    user_id: ObjectId

class PostPhoto(Base):
    url: str
    name: str
    description: str
    type: str = "post"
    likes: List = []
    comments: List[Comment] = []
    user_id: ObjectId