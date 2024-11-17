from app.core.database import database
from app.repository.base_repository import BaseRepository
from app.schema.face_schema import ListFaceRequest


class FaceRepository(BaseRepository):
    def __init__(self):
        super().__init__(database.get_collection("faces"))

    def list(self, request: ListFaceRequest):
        query = {"user_id": request.user_id}
        page = request.page if request.page else 1
        size = request.size if request.size else 10
        skip = (page - 1) * size

        faces_cursor = self.collection.aggregate([
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
        return faces_cursor, total