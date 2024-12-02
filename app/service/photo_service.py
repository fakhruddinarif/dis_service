from typing import Tuple, List
from urllib.parse import urlparse
from uuid import uuid4

from bson import ObjectId
from fastapi import UploadFile, HTTPException

from app.core.detector import face_detector
from app.core.facenet import facenet_model
from app.core.logger import logger

from app.core.config import config
from app.core.s3_client import s3_client
from app.model.photo_model import SellPhoto, PostPhoto
from app.repository.photo_repository import PhotoRepository
from app.schema.photo_schema import AddSellPhotoRequest, SellPhotoResponse, AddPostPhotoRequest, PostPhotoResponse, \
    GetPhotoRequest, DeletePhotoRequest, UpdatePostPhotoRequest, UpdateSellPhotoRequest, LikePhotoPostRequest, \
    ListPhotoRequest, CollectionPhotoRequest


class PhotoService:
    def __init__(self):
        self.photo_repository = PhotoRepository()

    def add_sell_photo(self, request: AddSellPhotoRequest, file: UploadFile) -> SellPhotoResponse:
        errors = {}
        logger.info(f"Add sell photo request: {request}")

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
                faces.append(
                    {"embeddings": face_embedding.tolist(), "box": {"x": x, "y": y, "width": width, "height": height}})
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
            raise HTTPException(status_code=400, detail=e)

    def add_post_photo(self, request: AddPostPhotoRequest, file: UploadFile) -> PostPhotoResponse:
        errors = {}
        logger.info(f"Add post photo request: {request}")
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
            logger.info(f"Add post photo response: {photo}")
            return PostPhotoResponse(**photo.dict(by_alias=True))
        except Exception as e:
            logger.error(f"Error during add post photo: {str(e)}")
            raise HTTPException(status_code=400, detail="Error during add post photo")

    def get(self, request: GetPhotoRequest):
        logger.info(f"Get photo request: {request}")
        try:
            photo = self.photo_repository.find_by_id(ObjectId(request.id))
            if not photo:
                raise HTTPException(status_code=404, detail="Photo not found")
            logger.info(f"Get photo response: {photo}")
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
        logger.info(f"List photo request: {request}")
        try:
            photos, total = self.photo_repository.list(request)
            logger.info(f"List photo response: {photos}")
            if request.type == "sell":
                for photo in photos:
                    photo["url"] = s3_client.get_object(config.aws_bucket, urlparse(photo["url"]).path.lstrip("/"))
                    photo["_id"] = str(photo["_id"])
                    photo["user_id"] = str(photo["user_id"])
                    photo["buyer_id"] = str(photo["buyer_id"]) if photo["buyer_id"] else None
                logger.info(f"List sell photo response: {photos}")
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
        logger.info(f"Update post photo request: {request}")
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
            logger.info(f"Update post photo response: {photo}")
            return PostPhotoResponse(**photo.dict(by_alias=True))
        except Exception as e:
            logger.error(f"Error during update post photo: {str(e)}")
            raise HTTPException(status_code=400, detail="Error during update post photo")

    def update_sell_photo(self, request: UpdateSellPhotoRequest) -> SellPhotoResponse:
        logger.info(f"Update sell photo request: {request}")
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
            logger.info(f"Update sell photo response: {photo}")
            return SellPhotoResponse(**photo.dict(by_alias=True))
        except Exception as e:
            logger.error(f"Error during update sell photo: {str(e)}")
            raise HTTPException(status_code=400, detail="Error during update sell photo")

    def delete(self, request: DeletePhotoRequest) -> bool:
        logger.info(f"Delete photo request: {request}")
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
                if photo:
                    raise HTTPException(status_code=400, detail="Photo already liked")
                result = self.photo_repository.add_like(ObjectId(request.id), ObjectId(request.user_id))
            else:
                if not photo:
                    raise HTTPException(status_code=400, detail="Photo not liked")
                result = self.photo_repository.remove_like(ObjectId(request.id), ObjectId(request.user_id))

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

    def sample_photos(self) -> List[dict]:
        try:
            photos = self.photo_repository.sample_photos()
            for photo in photos:
                photo["url"] = s3_client.get_object(config.aws_bucket, urlparse(photo["url"]).path.lstrip("/"))
                photo["_id"] = str(photo["_id"])
                photo["user_id"] = str(photo["user_id"])
                photo["likes"] = len(photo["likes"])
                photo["liked"] = False
            return [PostPhotoResponse(**photo).dict(by_alias=True) for photo in photos]
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