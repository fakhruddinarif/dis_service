from datetime import datetime, timedelta
from bson import ObjectId
from fastapi import HTTPException
from requests import request

from app.core.config import config
from app.model.transaction_model import Transaction
from app.repository.photo_repository import PhotoRepository
from app.repository.transaction_repository import TransactionRepository
from app.repository.user_repository import UserRepository
from app.schema.transaction_schema import TransactionRequest, TransactionResponse, PaymentMidtransRequest
from app.core.logger import logger

class TransactionService:
    def __init__(self):
        self.transaction_repository = TransactionRepository()
        self.photo_repository = PhotoRepository()
        self.user_repository = UserRepository()

    def create(self, request: TransactionRequest) -> TransactionResponse:
        errors = {}
        required_fields = {
            "buyer_id": "buyer ID is required",
            "photo_id": "photo IDs is required",
        }

        for field, error_message in required_fields.items():
            if not request.dict().get(field):
                errors[field] = error_message

        if errors:
            logger.error(f"Validation error: {errors}")
            raise HTTPException(status_code=400, detail=errors)

        try:
            buyer = self.user_repository.find_by_id(ObjectId(request.buyer_id))
            if not buyer:
                raise HTTPException(status_code=404, detail="User not found")

            total = 0
            for photo_id in request.photo_id:
                photo = self.photo_repository.find_by_id(ObjectId(photo_id))
                if not photo:
                    raise HTTPException(status_code=404, detail="Photo not found")
                total += photo["sell_price"]

            transaction = Transaction(
                buyer_id=ObjectId(request.buyer_id),
                photo_id=[ObjectId(photo_id) for photo_id in request.photo_id],
                total=total,
                date=datetime.now(),
                expired_at=datetime.now() + timedelta(minutes=5)
            )
            result = self.transaction_repository.create(transaction)
            transaction = self.transaction_repository.find_by_id(result.inserted_id)
            transaction["_id"] = str(transaction["_id"])
            transaction["buyer_id"] = str(transaction["buyer_id"])
            transaction["photo_id"] = [str(photo_id) for photo_id in transaction["photo_id"]]
            payment = self.qris_payment(transaction)
            transaction["payment"] = payment
            return TransactionResponse(**transaction)
        except Exception as e:
            logger.error(f"Error when creating transaction: {e}")
            raise HTTPException(status_code=500, detail="Internal server error")

    def qris_payment(self, transaction):
        server_key = config.server_key_sandbox if config.env == "local" else config.server_key_production
        headers = {
            "accept": "application/json",
            "content-type": "application/json",
            "Authorization": f"Basic {server_key}"
        }

        payload = {
            "payment_type": "qris",
            "transaction_details": {
                "order_id": transaction["_id"],
                "gross_amount": transaction["total"]
            }
        }

        response = request("POST", "https://api.sandbox.midtrans.com/v2/charge", headers=headers, json=PaymentMidtransRequest(**payload).dict())
        if response.status_code != 201:
            logger.error(f"Error when creating payment: {response.text}")
            raise HTTPException(status_code=500, detail="Failed to create payment")
        return response.json()