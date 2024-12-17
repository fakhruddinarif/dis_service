from io import BytesIO
from typing import Tuple, List
from urllib.parse import urlparse
from uuid import uuid4

from PIL import Image
from bson import ObjectId
from fastapi import UploadFile, HTTPException
from fastapi.responses import StreamingResponse
from app.repository.user_repository import UserRepository
from app.core.detector import face_detector
from app.core.facenet import facenet_model
from app.core.faiss_vector import FaissVector
from app.core.logger import logger
import numpy as np
from app.core.config import config
from app.core.s3_client import s3_client
from app.core.utils import create_watermark
from app.model.photo_model import SellPhoto, PostPhoto
from app.repository.face_repository import FaceRepository
from app.repository.photo_repository import PhotoRepository
from app.schema.photo_schema import AddSellPhotoRequest, SellPhotoResponse, AddPostPhotoRequest, PostPhotoResponse, \
    GetPhotoRequest, DeletePhotoRequest, UpdatePostPhotoRequest, UpdateSellPhotoRequest, LikePhotoPostRequest, \
    ListPhotoRequest, CollectionPhotoRequest, SamplePhotoResponse, SamplePhotoRequest


class PhotoService:
    def __init__(self):
        self.photo_repository = PhotoRepository()
        self.faiss_vector = FaissVector()
        self.face_repository = FaceRepository()
        self.user_repository = UserRepository()

    def add_sell_photo(self, request: AddSellPhotoRequest, file: UploadFile) -> SellPhotoResponse:
        errors = {}

        required_fields = {
            "name": "Name is required",
            "description": "Description is required",
            "base_price": "Price is required",
            "sell_price": "Price is required",
            "user_id": "User ID is required"
        }

        for field, error_message in required_fields.items():
            if not getattr(request, field):
                errors[field] = error_message

        if errors:
            logger.warning(f"Validation errors: {errors}")
            raise HTTPException(status_code=400, detail=errors)

        try:
            detected_faces = face_detector.detect_faces(file)
            if not detected_faces:
                raise HTTPException(status_code=400, detail="No face detected")
            faces = []
            for face, (x, y, width, height) in detected_faces:
                face_embedding = facenet_model.get_embeddings(face)
                logger.info(f"Length of face embedding: {len(face_embedding)}")
                self.faiss_vector.add(face_embedding)
                faiss_id = self.faiss_vector.index.ntotal - 1
                file.file.seek(0)
                watermark = create_watermark(file, [(x, y, width, height)])
                watermarked_image = Image.fromarray(watermark)
                watermarked_image_io = BytesIO()
                watermarked_image.save(watermarked_image_io, format='JPEG')
                watermarked_image_io.seek(0)
                file_path = f"watermark/{faiss_id}.jpg"
                s3_client.upload_file(watermarked_image_io, config.aws_bucket, file_path)
                faces.append(
                    {"embeddings": face_embedding.tolist(), "box": {"x": x, "y": y, "width": width, "height": height}, "faiss_id": faiss_id, "url": f"{config.aws_url}{file_path}"})
            request.detections = faces

            request.user_id = ObjectId(request.user_id)
            file_path = f"photos/sell/{uuid4()}_{file.filename}"
            file.file.seek(0)
            s3_client.upload_file(file.file, config.aws_bucket, file_path)
            request.url = f"{config.aws_url}{file_path}"
            photo = SellPhoto(**request.dict())
            result = self.photo_repository.create(photo)
            photo.id = str(result.inserted_id)
            photo.user_id = str(photo.user_id)
            return SellPhotoResponse(**photo.dict(by_alias=True))
        except Exception as e:
            logger.error(f"Error during add sell photo: {str(e)}")
            raise HTTPException(status_code=400, detail=str(e))

    def add_post_photo(self, request: AddPostPhotoRequest, file: UploadFile) -> PostPhotoResponse:
        errors = {}
        required_fields = {
            "name": "Name is required",
            "description": "Description is required",
            "user_id": "User ID is required"
        }

        for field, error_message in required_fields.items():
            if not getattr(request, field):
                errors[field] = error_message

        if errors:
            logger.warning(f"Validation errors: {errors}")
            raise HTTPException(status_code=400, detail=errors)

        try:
            file_path = f"photos/post/{uuid4()}_{file.filename}"
            file.file.seek(0)
            s3_client.upload_file(file.file, config.aws_bucket, file_path)
            request.url = f"{config.aws_url}{file_path}"
            request.user_id = ObjectId(request.user_id)
            photo = PostPhoto(**request.dict())
            result = self.photo_repository.create(photo)
            photo.id = str(result.inserted_id)
            photo.user_id = str(photo.user_id)
            photo.likes = len(photo.likes)
            return PostPhotoResponse(**photo.dict(by_alias=True))
        except Exception as e:
            logger.error(f"Error during add post photo: {str(e)}")
            raise HTTPException(status_code=400, detail="Error during add post photo")

    def get(self, request: GetPhotoRequest):
        try:
            photo = self.photo_repository.find_by_id(ObjectId(request.id))
            if not photo:
                raise HTTPException(status_code=404, detail="Photo not found")
            if isinstance(photo, dict):
                photo["url"] = s3_client.get_object(config.aws_bucket, urlparse(photo["url"]).path.lstrip("/"))
                if photo["type"] == "sell":
                    photo = SellPhoto(**photo)
                    photo.id = str(photo.id)
                    photo.user_id = str(photo.user_id)
                    photo.buyer_id = str(photo.buyer_id) if photo.buyer_id else None
                    return SellPhotoResponse(**photo.dict(by_alias=True))
                else:
                    photo = PostPhoto(**photo)
                    photo.id = str(photo.id)
                    photo.user_id = str(photo.user_id)
                    photo_dict = photo.dict(by_alias=True)
                    photo_dict["likes"] = len(photo.likes)
                    photo_dict["liked"] = True if ObjectId(request.user_id) in photo.likes else False
                    return PostPhotoResponse(**photo_dict)
            else:
                raise HTTPException(status_code=400, detail="Invalid photo data")
        except Exception as e:
            logger.error(f"Error during get photo: {str(e)}")
            raise HTTPException(status_code=400, detail="Error during get photo")

    def list(self, request: ListPhotoRequest) -> Tuple[List[dict], int]:
        try:
            photos, total = self.photo_repository.list(request)
            if request.type == "sell":
                for photo in photos:
                    photo["url"] = s3_client.get_object(config.aws_bucket, urlparse(photo["url"]).path.lstrip("/"))
                    photo["_id"] = str(photo["_id"])
                    photo["user_id"] = str(photo["user_id"])
                    photo["buyer_id"] = str(photo["buyer_id"]) if photo["buyer_id"] else None
                return [SellPhotoResponse(**photo).dict(by_alias=True) for photo in photos], total
            else:
                for photo in photos:
                    photo["url"] = s3_client.get_object(config.aws_bucket, urlparse(photo["url"]).path.lstrip("/"))
                    photo["_id"] = str(photo["_id"])
                    photo["user_id"] = str(photo["user_id"])
                    photo["liked"] = True if ObjectId(request.user_id) in photo["likes"] else False
                    photo["likes"] = len(photo["likes"])
                return [PostPhotoResponse(**photo).dict(by_alias=True) for photo in photos], total
        except Exception as e:
            logger.error(f"Error during list photo: {str(e)}")
            raise HTTPException(status_code=400, detail="Error during list photo")

    def update_post_photo(self, request: UpdatePostPhotoRequest) -> PostPhotoResponse:
        errors = {}
        required_fields = {
            "id": "ID is required",
            "name": "Name is required",
            "description": "Description is required",
            "user_id": "User ID is required"
        }

        for field, error_message in required_fields.items():
            if not getattr(request, field):
                errors[field] = error_message

        if errors:
            logger.warning(f"Validation errors: {errors}")
            raise HTTPException(status_code=400, detail=errors)

        try:
            photo = self.photo_repository.find_by_id(ObjectId(request.id))
            if not photo:
                raise HTTPException(status_code=404, detail="Photo not found")
            if photo["type"] == "sell":
                raise HTTPException(status_code=400, detail="Cannot update sell photo")
            photo = PostPhoto(**photo)
            photo.name = request.name
            photo.description = request.description
            photo.user_id = ObjectId(request.user_id)
            result = self.photo_repository.update(photo)
            if not result.modified_count:
                raise HTTPException(status_code=400, detail="Error during update photo")
            photo.id = str(photo.id)
            photo.user_id = str(photo.user_id)
            return PostPhotoResponse(**photo.dict(by_alias=True))
        except Exception as e:
            logger.error(f"Error during update post photo: {str(e)}")
            raise HTTPException(status_code=400, detail="Error during update post photo")

    def update_sell_photo(self, request: UpdateSellPhotoRequest) -> SellPhotoResponse:
        errors = {}
        required_fields = {
            "id": "ID is required",
            "name": "Name is required",
            "description": "Description is required",
            "base_price": "Price is required",
            "sell_price": "Price is required",
            "user_id": "User ID is required"
        }

        for field, error_message in required_fields.items():
            if not getattr(request, field):
                errors[field] = error_message

        if errors:
            logger.warning(f"Validation errors: {errors}")
            raise HTTPException(status_code=400, detail=errors)

        try:
            photo = self.photo_repository.find_by_id(ObjectId(request.id))
            if not photo:
                raise HTTPException(status_code=404, detail="Photo not found")
            if photo["type"] == "post":
                raise HTTPException(status_code=400, detail="Cannot update post photo")
            photo = SellPhoto(**photo)
            photo.name = request.name
            photo.description = request.description
            photo.base_price = request.base_price
            photo.sell_price = request.sell_price
            photo.user_id = ObjectId(request.user_id)
            result = self.photo_repository.update(photo)
            if not result.modified_count:
                raise HTTPException(status_code=400, detail="Error during update photo")
            photo.id = str(photo.id)
            photo.user_id = str(photo.user_id)
            photo.buyer_id = str(photo.buyer_id) if photo.buyer_id else None
            return SellPhotoResponse(**photo.dict(by_alias=True))
        except Exception as e:
            logger.error(f"Error during update sell photo: {str(e)}")
            raise HTTPException(status_code=400, detail="Error during update sell photo")

    def delete(self, request: DeletePhotoRequest) -> bool:
        try:
            photo = self.photo_repository.find_by_id(ObjectId(request.id))
            if not photo:
                raise HTTPException(status_code=404, detail="Photo not found")
            if photo["type"] == "sell":
                if photo["status"] == "sold":
                    raise HTTPException(status_code=400, detail="Cannot delete sold photo")
                if photo["status"] == "waiting":
                    raise HTTPException(status_code=400, detail="Cannot delete waiting photo")
                photo = SellPhoto(**photo)
            else:
                photo = PostPhoto(**photo)
            result = self.photo_repository.delete(photo)
            logger.info(f"Delete photo response: {result}")
            if result.deleted_count == 0:
                raise HTTPException(status_code=400, detail="Error during delete photo")
            return True
        except Exception as e:
            logger.error(f"Error during delete photo: {str(e)}")
            raise HTTPException(status_code=400, detail="Error during delete photo")

    def like_post(self, request: LikePhotoPostRequest):
        logger.info(f"Like post request: {request}")
        try:
            photo = self.photo_repository.find_like_by_user(ObjectId(request.id), ObjectId(request.user_id))
            logger.info(f"Like post photo: {photo}")
            if request.liked:
                if not photo:
                    raise HTTPException(status_code=400, detail="Photo not liked")
                result = self.photo_repository.remove_like(ObjectId(request.id), ObjectId(request.user_id))
            else:
                if photo:
                    raise HTTPException(status_code=400, detail="Photo already liked")
                result = self.photo_repository.add_like(ObjectId(request.id), ObjectId(request.user_id))

            if result.modified_count == 0:
                raise HTTPException(status_code=400, detail="Error during like post")
            photo = self.photo_repository.find_by_id(ObjectId(request.id))
            photo["liked"] = True if ObjectId(request.user_id) in photo["likes"] else False
            photo["likes"] = len(photo["likes"])
            photo["_id"] = str(photo["_id"])
            photo["user_id"] = str(photo["user_id"])
            logger.info(f"Like post photo response: {photo}")
            return PostPhotoResponse(**photo)
        except Exception as e:
            logger.error(f"Error during like post: {str(e)}")
            raise HTTPException(status_code=400, detail=e)

    def sample_photos(self, request: SamplePhotoRequest) -> List[dict]:
        try:
            photos = self.photo_repository.sample_photos()
            for photo in photos:
                user = self.user_repository.find_by_id(photo["user_id"], include=["username", "photo", "following"])
                photo["url"] = s3_client.get_object(config.aws_bucket, urlparse(photo["url"]).path.lstrip("/"))
                photo["_id"] = str(photo["_id"])
                photo["user_id"] = str(photo["user_id"])
                photo["liked"] = True if ObjectId(request.user_id) in photo["likes"] else False
                photo["likes"] = len(photo["likes"])
                photo["user_following"] = ObjectId(photo["user_id"]) in user["following"] if user["following"] else False
                photo["user_name"] = user["username"]
                photo["user_photo"] = s3_client.get_object(config.aws_bucket, urlparse(user["photo"]).path.lstrip("/")) if user["photo"] else None
            return [SamplePhotoResponse(**photo).dict(by_alias=True) for photo in photos]
        except Exception as e:
            logger.error(f"Error during sample photos: {str(e)}")
            raise HTTPException(status_code=400, detail="Error during sample photos")

    def collection_photos(self, request: CollectionPhotoRequest) -> Tuple[List[dict], int]:
        try:
            photos, total = self.photo_repository.collection_photos(request)
            for photo in photos:
                photo["url"] = s3_client.get_object(config.aws_bucket, urlparse(photo["url"]).path.lstrip("/"))
                photo["_id"] = str(photo["_id"])
                photo["user_id"] = str(photo["user_id"])
                photo["buyer_id"] = str(photo["buyer_id"]) if photo["buyer_id"] else None
            return [SellPhotoResponse(**photo).dict(by_alias=True) for photo in photos], total
        except Exception as e:
            logger.error(f"Error during collection photos: {str(e)}")
            raise HTTPException(status_code=400, detail="Error during collection photos")

    def findme(self, user_id: str) -> List[SellPhotoResponse]:
        try:
            face = self.face_repository.find_by_user_id(ObjectId(user_id))
            if not face:
                raise HTTPException(status_code=404, detail="Face not found")
            face_embedding = face["detections"][0]["embeddings"]
            distances, indices = self.faiss_vector.search(face_embedding, threshold=0.8)

            logger.info(f"Findme: {distances}, {indices}")
            matched_photos = []
            for distance, index in zip(distances, indices):
                data = self.photo_repository.find_by_faiss_id(int(index))
                photo = data[0] if data else None
                logger.info(f"Findme photo: {photo}")
                if photo and photo["status"] == "available":
                    photo["url"] = s3_client.get_object(config.aws_bucket, urlparse(photo["detections"][0]["url"]).path.lstrip("/"))
                    photo["_id"] = str(photo["_id"])
                    photo["user_id"] = str(photo["user_id"])
                    photo["buyer_id"] = str(photo["buyer_id"]) if photo["buyer_id"] else None
                    matched_photos.append(SellPhotoResponse(**photo).dict(by_alias=True))
            return matched_photos
        except Exception as e:
            logger.error(f"Error during findme: {str(e)}")
            raise HTTPException(status_code=400, detail=str(e))