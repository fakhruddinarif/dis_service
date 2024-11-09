from bson import ObjectId, Decimal128
from decimal import Decimal
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
    buyer_id: ObjectId = None

class PostPhoto(Base):
    url: str
    name: str
    description: str
    type: str = "post"
    user_id: ObjectId