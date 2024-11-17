from fastapi import UploadFile

from app.schema.base_schema import WebResponse
from app.schema.face_schema import AddFaceRequest, ListFaceRequest
from app.service.face_service import FaceService


class FaceController:
    def __init__(self):
        self.face_service = FaceService()

    def add(self, request: AddFaceRequest, file: UploadFile) -> WebResponse[dict]:
        face = self.face_service.add(request, file)
        return WebResponse(data=face.dict(by_alias=True))

    def list(self, request: ListFaceRequest):
        faces, total = self.face_service.list(request)
        return {"data": faces, "total": total}