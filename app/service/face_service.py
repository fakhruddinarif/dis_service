from typing import Tuple, List
from uuid import uuid4

from bson import ObjectId

from app.core.config import config
from app.core.logger import logger
from fastapi import UploadFile, HTTPException

from app.core.s3_client import s3_client
from app.model.face_model import Face
from app.repository.face_repository import FaceRepository
from app.schema.face_schema import AddFaceRequest, FaceResponse, ListFaceRequest


class FaceService:
    def __init__(self):
        self.face_repository = FaceRepository()

    def add(self, request: AddFaceRequest, file: UploadFile) -> FaceResponse:
        try:
            file_path = f"faces/{uuid4()}_{file.filename}.jpg"
            file.file.seek(0)
            s3_client.s3.upload_fileobj(file.file, config.aws_bucket, file_path, ExtraArgs={"ACL": "public-read"})
            request.url = f"{config.aws_url}{file_path}"
            request.user_id = ObjectId(request.user_id)
            face = Face(**request.dict())
            result = self.face_repository.create(face)
            face.id = result.inserted_id
            face.user_id = str(face.user_id)
            logger.info(f"Face added: {face.dict()}")
            return FaceResponse(**face.dict())
        except Exception as e:
            logger.error(f"Face add error: {e}")
            raise HTTPException(status_code=500, detail="Face add error")

    def list(self, request: ListFaceRequest) -> Tuple[List[FaceResponse], int]:
        logger.info(f"List faces: {request.dict()}")
        try:
            faces, total = self.face_repository.list(request)
            for face in faces:
                face["_id"] = str(face["_id"])
                face["user_id"] = str(face["user_id"])
            logger.info(f"Faces listed: {faces}")
            return [FaceResponse(**face) for face in faces], total
        except Exception as e:
            logger.error(f"List faces error: {e}")
            raise HTTPException(status_code=500, detail="List faces error")