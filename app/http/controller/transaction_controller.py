from requests import Response
from typing import List

from sqlalchemy.dialects.postgresql.psycopg import logger

from app.schema.base_schema import WebResponse
from app.schema.transaction_schema import TransactionRequest, TransactionResponse, GetTransactionRequest, \
    GetPaymentRequest, VerifySignatureRequest, ListTransactionRequest
from app.service.transaction_service import TransactionService


class TransactionController:
    def __init__(self):
        self.transaction_service = TransactionService()

    def create(self, request: TransactionRequest) -> WebResponse[TransactionResponse]:
        transaction = self.transaction_service.create(request)
        return WebResponse(data=transaction.dict(by_alias=True))

    def list_by_buyer(self, request: ListTransactionRequest):
        transactions, total = self.transaction_service.list_by_buyer(request)
        return {
            "data": transactions,
            "total": total
        }

    def list_by_seller(self, request: ListTransactionRequest):
        transactions, total = self.transaction_service.list_by_seller(request)
        return {
            "data": transactions,
            "total": total
        }

    def get(self, request: GetTransactionRequest) -> WebResponse[TransactionResponse]:
        transaction = self.transaction_service.get(request)
        return WebResponse(data=transaction.dict(by_alias=True))

    def get_payment(self, request: GetPaymentRequest) -> WebResponse[dict]:
        transaction = self.transaction_service.get_payment(request)
        return WebResponse(data=transaction)

    def payment_webhook(self, request: VerifySignatureRequest, payload: dict) -> WebResponse[TransactionResponse]:
        transaction = self.transaction_service.verify_payment(request, payload)
        return WebResponse(data=transaction.dict(by_alias=True))
