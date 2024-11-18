from fastapi import APIRouter, Body, Depends, HTTPException
from starlette.status import HTTP_201_CREATED

from app.http.controller.transaction_controller import TransactionController
from app.http.middleware.auth import get_current_user
from app.schema.base_schema import WebResponse
from app.schema.transaction_schema import TransactionResponse, TransactionRequest


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



    return transaction_router