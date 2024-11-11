from bson import ObjectId

from app.model.base_model import Base

class Face(Base):
    url: str
    embedding: list
    user_id: ObjectId