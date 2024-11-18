from app.schema.base_schema import WebResponse
from app.schema.transaction_schema import TransactionRequest, TransactionResponse
from app.service.transaction_service import TransactionService


class TransactionController:
    def __init__(self):
        self.transaction_service = TransactionService()

    def create(self, request: TransactionRequest) -> WebResponse[TransactionResponse]:
        transaction = self.transaction_service.create(request)
        return WebResponse(data=transaction.dict(by_alias=True))