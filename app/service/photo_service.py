from idlelib.iomenu import errors
from uuid import uuid4

from bson import ObjectId
from fastapi import UploadFile, HTTPException
from sqlalchemy.dialects.postgresql.psycopg import logger

from app.core.config import config
from app.core.s3_client import s3_client
from app.model.photo_model import SellPhoto, PostPhoto
from app.repository.photo_repository import PhotoRepository
from app.schema.photo_schema import AddSellPhotoRequest, SellPhotoResponse, AddPostPhotoRequest, PostPhotoResponse, \
    GetPhotoRequest


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
            file_path = f"photos/sell/{uuid4()}_{file.filename}"
            file.file.seek(0)
            s3_client.s3.upload_fileobj(file.file, config.aws_bucket, file_path, ExtraArgs={"ContentType": file.content_type})
            request.url = f"{config.aws_url}{file_path}"
            request.user_id = ObjectId(request.user_id)
            photo = SellPhoto(**request.dict())
            result = self.photo_repository.create(photo)
            photo.id = str(result.inserted_id)
            photo.user_id = str(photo.user_id)
            logger.info(f"Add sell photo response: {photo}")
            return SellPhotoResponse(**photo.dict(by_alias=True))
        except Exception as e:
            logger.error(f"Error during add sell photo: {str(e)}")
            raise HTTPException(status_code=400, detail="Error during add sell photo")

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
            s3_client.s3.upload_fileobj(file.file, config.aws_bucket, file_path, ExtraArgs={"ContentType": file.content_type})
            request.url = f"{config.aws_url}{file_path}"
            request.user_id = ObjectId(request.user_id)
            photo = PostPhoto(**request.dict())
            result = self.photo_repository.create(photo)
            photo.id = str(result.inserted_id)
            photo.user_id = str(photo.user_id)
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
                return PostPhotoResponse(**photo.dict(by_alias=True))
        except Exception as e:
            logger.error(f"Error during get photo: {str(e)}")
            raise HTTPException(status_code=400, detail="Error during get photo")