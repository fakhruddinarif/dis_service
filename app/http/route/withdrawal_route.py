import math

from app.core.logger import logger

from fastapi import APIRouter, Depends, HTTPException, Request
from starlette.status import HTTP_201_CREATED
from typing import List
from app.http.controller.withdrawal_controller import WithdrawalController
from app.http.middleware.auth import get_current_user
from app.schema.base_schema import WebResponse
from app.schema.withdrawal_schema import CreateWithdrawalRequest, WithdrawalResponse, ListWithdrawalRequest


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

    @withdrawal_router.get("/", response_model=WebResponse[List[WithdrawalResponse]])
    async def list(request: Request, current_user: str = Depends(get_current_user)):
        page = request.query_params.get("page", 1)
        size = request.query_params.get("size", 10)
        data = ListWithdrawalRequest()
        try:
            if current_user:
                data.user_id = current_user
            data.page = int(page)
            data.size = int(size)

            result = withdrawal_controller.list(data)
            total = result["total"]
            paging = {
                "page": data.page,
                "size": data.size,
                "total_item": total,
                "total_page": int(math.ceil(total / data.size))
            }
            return WebResponse(data=result["data"], paging=paging)
        except Exception as e:
            logger.error(f"Failed to list withdrawal: {e}")
            raise HTTPException(status_code=500, detail=str(e))

    return withdrawal_router