import base64
import math
from datetime import datetime, timedelta
import requests
from bson import ObjectId
from fastapi import HTTPException
from pymongo.results import UpdateResult

from app.core.config import config
from app.core.security import get_encoded_server_key
from app.model.transaction_model import Transaction, Payment
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
                total=math.ceil(total),
            )
            result = self.transaction_repository.create(transaction)
            transaction = self.transaction_repository.find_by_id(result.inserted_id)
            payment = self.qris_payment(transaction)
            logger.info(f"Payment: {payment}")
            payment_payload = {
                "_id": payment["transaction_id"],
                "status": payment["transaction_status"],
                "qris": payment["actions"][0]["url"],
                "expired_at": payment["expiry_time"]
            }
            transaction["payment"] = Payment(**payment_payload)
            transaction = Transaction(**transaction)
            update_Result: UpdateResult = self.transaction_repository.update(transaction)
            if update_Result.modified_count == 0:
                raise HTTPException(status_code=500, detail="Failed to update transaction")
            updated_transaction = self.transaction_repository.find_by_id(result.inserted_id)
            logger.info(f"Transaction: {updated_transaction}")
            updated_transaction["_id"] = str(updated_transaction["_id"])
            updated_transaction["buyer_id"] = str(updated_transaction["buyer_id"])
            updated_transaction["photo_id"] = [str(photo_id) for photo_id in updated_transaction["photo_id"]]
            return TransactionResponse(**updated_transaction)
        except Exception as e:
            logger.error(f"Error when creating transaction: {e}")
            raise HTTPException(status_code=500, detail=e)

    def get(self):
        transaction = {
            "_id": "5f7f1b3b7b3b3b3b3b3b3b3b",
            "buyer_id": "5f7f1b3b7b3b3b3b3b3b3b3b",
            "details": [
                {
                    "seller_id": "5f7f1b3b7b3b3b3b3b3b3b3b",
                    "photo_id": [
                        "5f7f1b3b7b3b3b3b3b3b3b3b",
                        "5f7f1b3b7b3b3b3b3b3b3b3b",
                        "5f7f1b3b7b3b3b3b3b3b3b3b"
                    ],
                    "total": 300000
                },
                {
                    "seller_id": "5f7f1b3b7b3b3b3b3b3b3b3b",
                    "photo_id": [
                        "5f7f1b3b7b3b3b3b3b3b3b3b",
                        "5f7f1b3b7b3b3b3b3b3b3b3b",
                        "5f7f1b3b7b3b3b3b3b3b3b3b"
                    ],
                    "total": 300000
                }
            ],
            "total": 600000,
            "status": "pending",
            "date": "2020-10-08T00:00:00",
            "payment": {
                "_id": "5f7f1b3b7b3b3b3b3b3b3b3b",
                "status": "pending",
                "type": "qris",
                "url": "https://example.com",
                "expired_at": "2020-10-08T00:00:00"
            },
        }

    def list(self):
        pass

    def update(self):
        pass

    def get_payment(self):
        pass

    def verify_payment(self):
        pass

    def qris_payment(self, transaction):
        server_key = get_encoded_server_key()
        url = config.url_sandbox
        headers = {
            "accept": "application/json",
            "content-type": "application/json",
            "Authorization": f"Basic {server_key}:"
        }

        payload = {
            "payment_type": "qris",
            "transaction_details": {
                "order_id": str(transaction["_id"]),
                "gross_amount": math.ceil(transaction["total"])
            },
            "qris": {"acquirer": "gopay"}
        }

        response = requests.post(url, headers=headers, json=PaymentMidtransRequest(**payload).dict())
        return response.json()