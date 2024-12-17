from bson import ObjectId
from app.core.logger import logger
from app.core.database import database
from app.repository.base_repository import BaseRepository
from app.schema.cart_schema import ListItemRequest


class CartRepository(BaseRepository):
    def __init__(self):
        super().__init__(database.get_collection("carts"))

    def find_by_user_id(self, user_id: ObjectId):
        return self.collection.find_one({"user_id": user_id})

    def remove_photo(self, user_id: ObjectId, photo_id: ObjectId):
        query = {"user_id": user_id}
        update = {"$pull": {"photos": photo_id}}
        self.collection.update_one(query, update)

    def list(self, request: ListItemRequest):
        query = {"user_id": ObjectId(request.user_id)}
        page = request.page if request.page else 1
        size = request.size if request.size else 10
        skip = (page - 1) * size

        carts_cursor = self.collection.aggregate([
            {"$match": query},
            {"$unwind": "$photos"},
            {"$sort": {"created_at": -1}},
            {"$skip": skip},
            {"$limit": size},
            {"$group": {"_id": None, "photos": {"$push": "$photos"}}},
            {"$project": {"_id": 0, "photos": 1}}
        ])
        total_pipeline = [
            {"$match": query},
            {"$unwind": "$photos"},
            {"$count": "total"}
        ]
        total_cursor = self.collection.aggregate(total_pipeline)
        total = list(total_cursor)
        total = total[0]["total"] if total else 0
        carts = list(carts_cursor)
        return carts[0]["photos"] if carts else [], total