from bson import ObjectId
from pydantic import BaseModel

from app.model.base_model import Base

class BoundBox(BaseModel):
    x: float
    y: float
    width: float
    height: float

class Detections(BaseModel):
    embeddings: list = []
    box: BoundBox

class Face(Base):
    url: str
    detections: list[Detections] = []
    user_id: ObjectId