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
        query = {"details.seller_id": ObjectId(request.user_id)}
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