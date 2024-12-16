from typing import Tuple, List
from urllib.parse import urlparse
from uuid import uuid4

from bson import ObjectId

from app.core.config import config
from app.core.detector import FaceDetector, face_detector
from app.core.facenet import FaceNetModel, facenet_model
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
            logger.info(f"Add face: {request.dict()}")
            detected_faces = face_detector.detect_faces(file)
            if not detected_faces:
                raise HTTPException(status_code=400, detail="No face detected")
            if len(detected_faces) > 1:
                raise HTTPException(status_code=400, detail="Multiple faces detected")
            detected_face, (x, y, width, height) = detected_faces[0]
            detected_embedding = facenet_model.get_embeddings(detected_face)

            request.user_id = ObjectId(request.user_id)
            request.detections = [{"embeddings": detected_embedding.tolist(), "box": {"x": x, "y": y, "width": width, "height": height}}]
            file_path = f"faces/{uuid4()}_{file.filename}"
            file.file.seek(0)
            s3_client.s3.upload_fileobj(file.file, config.aws_bucket, file_path, ExtraArgs={"ACL": "public-read"})
            request.url = f"{config.aws_url}{file_path}"
            face = Face(**request.dict())
            result = self.face_repository.create(face)
            face.id = str(result.inserted_id)
            face.user_id = str(face.user_id)
            return FaceResponse(**face.dict(by_alias=True))
        except Exception as e:
            logger.error(f"Face add error: {e}")
            raise HTTPException(status_code=500, detail=e)

    def list(self, request: ListFaceRequest) -> Tuple[List[FaceResponse], int]:
        logger.info(f"List faces: {request.dict()}")
        try:
            faces, total = self.face_repository.list(request)
            for face in faces:
                face["url"] = s3_client.get_object(config.aws_bucket, urlparse(face["url"]).path.lstrip("/"))
                face["_id"] = str(face["_id"])
                face["user_id"] = str(face["user_id"])
            return [FaceResponse(**face) for face in faces], total
        except Exception as e:
            logger.error(f"List faces error: {e}")
            raise HTTPException(status_code=500, detail="List faces error")

    def detect_face(self, file: UploadFile) -> bool:
        try:
            detected_faces = face_detector.detect_faces(file)
            if not detected_faces:
                raise HTTPException(status_code=400, detail="Face not detected")
            if len(detected_faces) > 1:
                raise HTTPException(status_code=400, detail="Multiple faces detected")
            return True
        except Exception as e:
            logger.error(f"Face detection error: {e}")
            raise HTTPException(status_code=500, detail=str(e))