from bson import ObjectId

from app.core.database import database
from app.repository.base_repository import BaseRepository
from app.schema.withdrawal_schema import ListWithdrawalRequest


class WithdrawalRepository(BaseRepository):
    def __init__(self):
        super().__init__(database.get_collection("withdrawals"))

    def list(self, request: ListWithdrawalRequest):
        page = request.page if request.page else 1
        size = request.size if request.size else 10
        skip = (page - 1) * size

        withdrawal_cursor = self.collection.aggregate([
            {"$skip": skip},
            {"$limit": size},
        ])

        withdrawals = list(withdrawal_cursor)
        total_withdrawals = self.collection.count_documents({})

        return withdrawals, total_withdrawals