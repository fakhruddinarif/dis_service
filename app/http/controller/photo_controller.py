from fastapi import UploadFile

from app.schema.base_schema import WebResponse
from app.schema.photo_schema import AddSellPhotoRequest, AddPostPhotoRequest, GetPhotoRequest, UpdateSellPhotoRequest, \
    SellPhotoResponse, PostPhotoResponse, UpdatePostPhotoRequest, DeletePhotoRequest, LikePhotoPostRequest, \
    ListPhotoRequest, CollectionPhotoRequest
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

    def get(self, request: GetPhotoRequest) -> WebResponse[dict]:
        photo = self.photo_service.get(request)
        return WebResponse(data=photo.dict(by_alias=True))

    def list(self, request: ListPhotoRequest):
        photos, total = self.photo_service.list(request)
        return {"data": photos, "total": total}

    def update_post(self, request: UpdatePostPhotoRequest) -> WebResponse[PostPhotoResponse]:
        photo = self.photo_service.update_post_photo(request)
        return WebResponse(data=photo.dict(by_alias=True))

    def update_sell(self, request: UpdateSellPhotoRequest) -> WebResponse[SellPhotoResponse]:
        photo = self.photo_service.update_sell_photo(request)
        return WebResponse(data=photo.dict(by_alias=True))

    def delete(self, request: DeletePhotoRequest) -> WebResponse[bool]:
        photo = self.photo_service.delete(request)
        return WebResponse(data=photo)

    def like(self, request: LikePhotoPostRequest) -> WebResponse[PostPhotoResponse]:
        photo = self.photo_service.like_post(request)
        return WebResponse(data=photo)

    def sample_photos(self) -> WebResponse[dict]:
        photos = self.photo_service.sample_photos()
        return WebResponse(data=photos)

    def collection_photos(self, request: CollectionPhotoRequest):
        photos, total = self.photo_service.collection_photos(request)
        return {"data": photos, "total": total}