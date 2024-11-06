from app.service.photo_service import PhotoService


class PhotoController:
    def __init__(self):
        self.photo_service = PhotoService()

    def add_sell_photo(self, request, file):
        return self.photo_service.add_sell_photo(request, file)

    def add_post_photo(self, request, file):
        return self.photo_service.add_post_photo(request, file)