from app.schema.base_schema import WebResponse
from app.schema.withdrawal_schema import CreateWithdrawalRequest, WithdrawalResponse, ListWithdrawalRequest
from app.service.withdrawal_service import WithdrawalService
from typing import List


class WithdrawalController:
    def __init__(self):
        self.withdrawal_service = WithdrawalService()

    def create(self, request: CreateWithdrawalRequest) -> WebResponse[WithdrawalResponse]:
        result = self.withdrawal_service.create(request)
        return WebResponse(data=result)

    def list(self, request: ListWithdrawalRequest) -> dict:
        withdrawals, total = self.withdrawal_service.list(request)
        return {"data": withdrawals, "total": total}