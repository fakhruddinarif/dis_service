from typing import Optional

from fastapi import Form, UploadFile, File
from pydantic import BaseModel, Field


class FaceResponse(BaseModel):
    id: str = Field(None, alias="_id")
    url: str
    embedding: list
    user_id: str

class AddFaceRequest(BaseModel):
    url: Optional[str] = None
    embedding: Optional[list] = []
    user_id: Optional[str] = None
    file: Optional[UploadFile]

    @classmethod
    def as_form(
        cls,
        url: Optional[str] = Form(None),
        user_id: Optional[str] = Form(None),
        embedding: Optional[list] = Form([]),
        file: UploadFile = File(...),
    ):
        return cls(url=url, user_id=user_id, embedding=embedding, file=file)

class ListFaceRequest(BaseModel):
    user_id: Optional[str] = None
    page: int = 1
    size: int = 10

class DeleteFaceRequest(BaseModel):
    id: Optional[str] = None
    user_id: Optional[str] = None