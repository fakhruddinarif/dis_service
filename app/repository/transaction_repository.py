from bson import ObjectId

from app.core.database import database
from app.repository.base_repository import BaseRepository
from app.schema.transaction_schema import ListTransactionRequest


class TransactionRepository(BaseRepository):
    def __init__(self):
        super().__init__(database.get_collection("transactions"))
    
    def list_by_buyer(self, request: ListTransactionRequest):
        query = {"buyer_id": ObjectId(request.user_id)}
        page = request.page if request.page else 1
        size = request.size if request.size else 10
        skip = (page - 1) * size

        transactions_cursor = self.collection.aggregate([
            {"$match": query},
            {"$sort": {"date": -1}},
            {"$skip": skip},
            {"$limit": size}
        ])

        total_pipeline = [
            {"$match": query},
            {"$group": {"_id": None, "total": {"$sum": 1}}},
        ]

        total_result = list(self.collection.aggregate(total_pipeline))
        total = total_result[0]["total"] if total_result else 0
        transactions = [transaction for transaction in transactions_cursor]
        return transactions, total

    def list_by_seller(self, request: ListTransactionRequest):
        query = {"details.seller_id": ObjectId(request.user_id), "status": "paid"}
        page = request.page if request.page else 1
        size = request.size if request.size else 10
        skip = (page - 1) * size

        transactions_cursor = self.collection.aggregate([
            {"$unwind": "$details"},
            {"$unwind": "$details.photo_id"},
            {"$match": query},
            {"$sort": {"date": -1}},
            {"$skip": skip},
            {"$limit": size},
            {"$group": {
                "_id": "$_id",
                "date": {"$first": "$date"},
                "buyer_id": {"$first": "$buyer_id"},
                "photo_ids": {"$push": "$details.photo_id"}
            }},
            {"$project": {"_id": 0, "date": 1, "buyer_id": 1, "photo_ids": 1}}
        ])

        total_pipeline = [
            {"$unwind": "$details"},
            {"$unwind": "$details.photo_id"},
            {"$match": query},
            {"$group": {"_id": None, "total": {"$sum": 1}}}
        ]

        total_result = list(self.collection.aggregate(total_pipeline))
        total = total_result[0]["total"] if total_result else 0
        transactions = [transaction for transaction in transactions_cursor]
        return transactions, total

    def find_by_payment_id(self, payment_id: str):
        return self.collection.find_one({"payment._id": payment_id})