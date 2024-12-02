from typing import Optional

from bson import ObjectId
from fastapi import Form, UploadFile, File
from pydantic import BaseModel, Field

from app.model.face_model import Detections


class FaceResponse(BaseModel):
    id: str = Field(ObjectId, alias="_id")
    url: str
    user_id: str

    class Config:
        from_attributes = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}

class AddFaceRequest(BaseModel):
    url: Optional[str] = None
    detections: Optional[Detections] = None
    user_id: Optional[str] = None
    file: Optional[UploadFile]

    @classmethod
    def as_form(
        cls,
        url: Optional[str] = Form(None),
        user_id: Optional[str] = Form(None),
        detections: Optional[Detections] = Form(None),
        file: UploadFile = File(...),
    ):
        return cls(url=url, user_id=user_id, detections=detections, file=file)

class ListFaceRequest(BaseModel):
    user_id: Optional[str] = None
    page: int = 1
    size: int = 10

class DeleteFaceRequest(BaseModel):
    id: Optional[str] = None
    user_id: Optional[str] = None