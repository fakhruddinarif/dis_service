from bson import ObjectId, Decimal128
from decimal import Decimal
from app.model.base_model import Base

class Photo(Base):
    url: str
    name: str
    base_price: Decimal128(Decimal("0.00"))
    sell_price: Decimal128(Decimal("0.00"))
    description: str
    user_id: ObjectId