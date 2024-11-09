from fastapi import UploadFile

from app.schema.base_schema import WebResponse
from app.schema.photo_schema import AddSellPhotoRequest, AddPostPhotoRequest
from app.service.photo_service import PhotoService


class PhotoController:
    def __init__(self):
        self.photo_service = PhotoService()

    def add_sell_photo(self, request: AddSellPhotoRequest, file: UploadFile) -> WebResponse[dict]:
        photo = self.photo_service.add_sell_photo(request, file)
        return WebResponse(data=photo.dict(by_alias=True))

    def add_post_photo(self, request: AddPostPhotoRequest, file: UploadFile) -> WebResponse[dict]:
        photo = self.photo_service.add_post_photo(request, file)
        return WebResponse(data=photo.dict(by_alias=True))