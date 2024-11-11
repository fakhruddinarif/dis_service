from bson import ObjectId

from app.core.database import database
from app.repository.base_repository import BaseRepository


class PhotoRepository(BaseRepository):
    def __init__(self):
        super().__init__(database.get_collection("photos"))

    def find_photo_by_id(self, id: ObjectId, user_id: ObjectId):
        return self.collection.find_one({"_id": id, "user_id": user_id})