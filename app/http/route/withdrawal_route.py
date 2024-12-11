from app.core.logger import logger

from fastapi import APIRouter, Depends, HTTPException
from starlette.status import HTTP_201_CREATED

from app.http.controller.withdrawal_controller import WithdrawalController
from app.http.middleware.auth import get_current_user
from app.schema.base_schema import WebResponse
from app.schema.withdrawal_schema import CreateWithdrawalRequest, WithdrawalResponse


def get_withdrawal_router():
    withdrawal_router = APIRouter()
    withdrawal_controller = WithdrawalController()

    @withdrawal_router.post("/", response_model=WebResponse[WithdrawalResponse], status_code=HTTP_201_CREATED)
    async def create(request: CreateWithdrawalRequest, current_user: str = Depends(get_current_user)):
        if current_user:
            request.user_id = current_user

        try:
            return withdrawal_controller.create(request)
        except Exception as e:
            logger.error(f"Failed to create withdrawal: {e}")
            raise HTTPException(status_code=500, detail=str(e))

    return withdrawal_router