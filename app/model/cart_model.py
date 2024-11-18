from bson import ObjectId

from app.model.base_model import Base
from typing import List

class Cart(Base):
    photos: List[ObjectId] = []
    user_id: ObjectId