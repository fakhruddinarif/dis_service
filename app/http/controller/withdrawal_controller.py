from app.schema.base_schema import WebResponse
from app.schema.withdrawal_schema import CreateWithdrawalRequest, WithdrawalResponse
from app.service.withdrawal_service import WithdrawalService


class WithdrawalController:
    def __init__(self):
        self.withdrawal_service = WithdrawalService()

    def create(self, request: CreateWithdrawalRequest) -> WebResponse[WithdrawalResponse]:
        result = self.withdrawal_service.create(request)
        return WebResponse(data=result)