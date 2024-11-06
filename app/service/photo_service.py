from uuid import uuid4

from fastapi import UploadFile, HTTPException
from sqlalchemy.dialects.postgresql.psycopg import logger

from app.core.config import config
from app.core.s3_client import s3_client
from app.model.photo_model import SellPhoto
from app.repository.photo_repository import PhotoRepository
from app.schema.photo_schema import AddSellPhotoRequest, SellPhotoResponse, AddPostPhotoRequest, PostPhotoResponse


class PhotoService:
    def __init__(self):
        self.photo_repository = PhotoRepository()

    def add_sell_photo(self, request: AddSellPhotoRequest, file: UploadFile) -> SellPhotoResponse:
        errors = {}
        logger.info(f"Add sell photo request: {request}")
        required_fields = {
            "url": "URL is required",
            "name": "Name is required",
            "base_price": "Base price is required",
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
            file_path = f"photos/sell/{uuid4()}_{file.filename}"
            file.file.seek(0)
            s3_client.s3.upload_fileobj(file.file, s3_client.bucket_name, file_path, ExtraArgs={"ContentType": file.content_type})
            request.url = f"{config.aws_url}{file_path}"

            admin_fee = request.base_price * 0.1
            data = {
                "url": request.url,
                "name": request.name,
                "base_price": request.base_price,
                "sell_price": request.base_price + admin_fee,
                "description": request.description,
                "user_id": request.user_id
            }
            photo = SellPhoto(**data)
            result = self.photo_repository.create(photo)
            photo._id = str(result.inserted_id)
            logger.info(f"Add sell photo response: {photo}")
            return SellPhotoResponse(**photo.dict(by_alias=True))
        except Exception as e:
            logger.error(f"Error during add sell photo: {str(e)}")
            raise HTTPException(status_code=400, detail="Error during add sell photo")

    def add_post_photo(self, request: AddPostPhotoRequest, file: UploadFile) -> PostPhotoResponse:
        errors = {}
        logger.info(f"Add post photo request: {request}")
        required_fields = {
            "url": "URL is required",
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
            s3_client.s3.upload_fileobj(file.file, s3_client.bucket_name, file_path, ExtraArgs={"ContentType": file.content_type})
            request.url = f"{config.aws_url}{file_path}"
            photo = SellPhoto(**request.dict())
            result = self.photo_repository.create(photo)
            photo._id = str(result.inserted_id)
            logger.info(f"Add post photo response: {photo}")
            return PostPhotoResponse(**photo.dict(by_alias=True))
        except Exception as e:
            logger.error(f"Error during add post photo: {str(e)}")
            raise HTTPException(status_code=400, detail="Error during add post photo")