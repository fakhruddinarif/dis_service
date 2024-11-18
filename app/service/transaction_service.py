from bson import ObjectId
from fastapi import HTTPException
from app.model.transaction_model import Transaction
from app.repository.photo_repository import PhotoRepository
from app.repository.transaction_repository import TransactionRepository
from app.repository.user_repository import UserRepository
from app.schema.transaction_schema import TransactionRequest, TransactionResponse
from app.core.logger import logger


class TransactionService:
    def __init__(self):
        self.transaction_repository = TransactionRepository()
        self.photo_repository = PhotoRepository()
        self.user_repository = UserRepository()

    def create(self, request: TransactionRequest, payload: dict) -> dict:
        errors = {}
        logger.info(f"Creating transaction with request: {request}")
        required_fields = {
            "buyer_id": "Buyer ID is required",
            "photo_id": "Photo ID is required",
            "total": "Total is required",
        }

        for field, message in required_fields.items():
            if not getattr(request, field):
                errors[field] = message

        if errors:
            logger.error(f"Error creating transaction: {errors}")
            raise HTTPException(status_code=400, detail=errors)

        user = self.user_repository.find_by_id(ObjectId(request.buyer_id), include=["id"])
        if not user:
            logger.error(f"Error creating transaction: User not found")
            raise HTTPException(status_code=404, detail="User not found")

        try:
            transaction = Transaction(**request.dict())
            result = self.transaction_repository.create(transaction)
            transaction.id = str(result.inserted_id)
            transaction.buyer_id = str(transaction.buyer_id)
            transaction.photo_id = [str(photo_id) for photo_id in transaction.photo_id]
            return transaction.dict(by_alias=True)
        except Exception as e:
            logger.error(f"Error creating transaction: {e}")
            raise HTTPException(status_code=500, detail="Internal server error")
