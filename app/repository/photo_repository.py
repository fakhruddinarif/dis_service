from bson import ObjectId

from app.core.database import database
from app.repository.base_repository import BaseRepository
from app.schema.photo_schema import ListPhotoRequest


class PhotoRepository(BaseRepository):
    def __init__(self):
        super().__init__(database.get_collection("photos"))

    def find_photo_by_id(self, id: ObjectId, user_id: ObjectId):
        return self.collection.find_one({"_id": id, "user_id": user_id})

    def find_photo_by_type(self, photo_type: str, user_id: ObjectId = None):
        query = {"type": photo_type}
        if user_id:
            query.update({"user_id": user_id})
        return self.collection.find(query)

    def find_like_by_user(self, id: ObjectId, user_id: ObjectId):
        return self.collection.find({"_id": id, "likes": user_id}, {"_id": 0, "likes": {"$elemMatch": {"$eq": user_id}}})

    def remove_like(self, id: ObjectId, user_id: ObjectId):
        return self.collection.update_one({"_id": id}, {"$pull": {"likes": user_id}})

    def add_like(self, id: ObjectId, user_id: ObjectId):
        return self.collection.update_one({"_id": id}, {"$push": {"likes": user_id}})

    def count_likes(self, id: ObjectId):
        return self.collection.aggregate([
            {"$match": {"_id": id}},
            {"$unwind": "$likes"},
            {"$group": {"_id": "$_id", "likes": {"$sum": 1}}},
            {"$project": {"_id": 0, "likes": 1}}
        ])

    def filter(self, request: ListPhotoRequest):
        query = {"user_id": ObjectId(request.user_id)}
        query.update({"type": request.type})
        return query

    def list(self, request: ListPhotoRequest):
        query = self.filter(request)
        page = request.page if request.page else 1
        size = request.size if request.size else 10
        skip = (page - 1) * size

        photos_cursor = self.collection.aggregate([
            {"$match": query},
            {"$skip": skip},
            {"$limit": size}
        ])
        total_pipeline = [
            {"$match": query},
            {"$group": {"_id": None, "total": {"$sum": 1}}}
        ]
        total = list(self.collection.aggregate(total_pipeline))
        total = total[0]["total"] if total else 0
        return photos_cursor, total