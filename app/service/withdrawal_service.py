from typing import Tuple

from bson import ObjectId
from fastapi import HTTPException
from pymongo.results import UpdateResult

from app.model.withdrawal_model import Withdrawal, WithdrawalStatus
from app.repository.user_repository import UserRepository
from app.repository.withdrawal_repository import WithdrawalRepository
from app.schema.withdrawal_schema import CreateWithdrawalRequest, WithdrawalResponse, ListWithdrawalRequest
from app.core.logger import logger

class WithdrawalService:
    def __init__(self):
        self.withdrawal_repository = WithdrawalRepository()
        self.user_repository = UserRepository()

    def create(self, request: CreateWithdrawalRequest) -> WithdrawalResponse:
        logger.info(f"Request received: {request.dict()}")
        errors = {}

        required_fields = {
            "account_id": "Account ID is required",
            "amount": "Amount is required",
            "user_id": "User ID is required"
        }

        for field, message in required_fields.items():
            if not getattr(request, field):
                errors[field] = message

        if errors:
            logger.warning(f"Validation error: {errors}")
            raise HTTPException(status_code=400, detail=errors)

        try:
            user_id = ObjectId(request.user_id)
            account_id = ObjectId(request.account_id)

            user = self.user_repository.find_by_id(user_id)
            if not user:
                raise HTTPException(status_code=404, detail="User not found")
            account = self.user_repository.find_account_by_id(user_id, account_id)
            if not account:
                raise HTTPException(status_code=404, detail="Account not found")

            if user["balance"] < request.amount or request.amount <= 0:
                raise HTTPException(status_code=400, detail="Insufficient balance")

            withdrawal = Withdrawal(
                user_id=user_id,
                account_id=account_id,
                amount=request.amount,
            )
            result = self.withdrawal_repository.create(withdrawal)
            user["balance"] -= request.amount
            result_balance = self.user_repository.update_balance(user_id, user["balance"])
            if result_balance.modified_count == 0:
                raise HTTPException(status_code=500, detail="Failed to update balance")
            withdrawal.id = str(result.inserted_id)
            withdrawal.user_id = str(withdrawal.user_id)
            withdrawal.account_id = str(withdrawal.account_id)
            return WithdrawalResponse(**withdrawal.dict(by_alias=True))
        except Exception as e:
            logger.error(f"Failed to create withdrawal: {e}")
            raise HTTPException(status_code=500, detail=str(e))
