import math
from venv import logger

from fastapi import APIRouter, Body, Depends, HTTPException, Request, Header
from starlette.status import HTTP_201_CREATED
from typing import List
from app.http.controller.transaction_controller import TransactionController
from app.http.middleware.auth import get_current_user
from app.schema.base_schema import WebResponse
from app.schema.transaction_schema import TransactionResponse, TransactionRequest, GetTransactionRequest, \
    GetPaymentRequest, VerifySignatureRequest, ListTransactionRequest, TransactionHistoryResponse, \
    TransactionHistoryBySellerResponse


def get_transaction_router():
    transaction_router = APIRouter()
    transaction_controller = TransactionController()

    @transaction_router.post("/", response_model=WebResponse[TransactionResponse], status_code=HTTP_201_CREATED)
    async def create(request: TransactionRequest = Body(...), current_user: str = Depends(get_current_user)):
        if current_user:
            request.buyer_id = current_user
        try:
            return transaction_controller.create(request)
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    @transaction_router.get("/buyer", response_model=WebResponse[List[TransactionHistoryResponse]])
    async def list_by_buyer(request: Request, current_user: str = Depends(get_current_user)):
        data = ListTransactionRequest()
        page = request.query_params.get("page", 1)
        size = request.query_params.get("size", 10)
        try:
            if current_user:
                data.user_id = current_user
            data.page = int(page)
            data.size = int(size)
            result = transaction_controller.list_by_buyer(data)
            total = result.get("total")
            paging = {
                "page": data.page,
                "size": data.size,
                "total_item": total,
                "total_page": int(math.ceil(total / data.size))
            }
            return WebResponse(data=result.get("data"), paging=paging)
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    @transaction_router.get("/seller", response_model=WebResponse[List[TransactionHistoryBySellerResponse]])
    async def list_by_seller(request: Request, current_user: str = Depends(get_current_user)):
        data = ListTransactionRequest()
        page = request.query_params.get("page", 1)
        size = request.query_params.get("size", 10)
        try:
            if current_user:
                data.user_id = current_user
            data.page = int(page)
            data.size = int(size)
            result = transaction_controller.list_by_seller(data)
            total = result.get("total")
            paging = {
                "page": data.page,
                "size": data.size,
                "total_item": total,
                "total_page": int(math.ceil(total / data.size))
            }
            return WebResponse(data=result.get("data"), paging=paging)
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    @transaction_router.get("/{id}", response_model=WebResponse[TransactionResponse])
    async def get(id, current_user: str = Depends(get_current_user)):
        try:
            request = GetTransactionRequest()
            if current_user:
                request.user_id = current_user
                request.id = id
            else:
                raise HTTPException(status_code=400, detail="Invalid user")
            return transaction_controller.get(request)
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    @transaction_router.get("/{id}/payment", response_model=WebResponse[dict])
    async def get_payment(id, current_user: str = Depends(get_current_user)):
        try:
            request = GetPaymentRequest()
            if current_user:
                request.user_id = current_user
                request.id = id
            else:
                raise HTTPException(status_code=400, detail="Invalid user")
            return transaction_controller.get_payment(request)
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    @transaction_router.post("/webhook/payment")
    async def verify_payment(request: Request):
        try:
            payload = await request.json()
            logger.info(f"Payload: {payload}")
            data = VerifySignatureRequest(
                transaction_id=payload.get("transaction_id"),
                status_code=payload.get("status_code"),
                gross_amount=payload.get("gross_amount"),
                signature=payload.get("signature_key")
            )
            return transaction_controller.payment_webhook(data, payload)
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    return transaction_router