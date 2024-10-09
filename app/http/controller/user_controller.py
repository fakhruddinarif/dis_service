from builtins import Exception

from fastapi import HTTPException

from app.schema.base_schema import WebResponse
from app.schema.user_schema import RegisterUserRequest
from app.service.user_service import UserService


class UserController:
    def __init__(self):
        self.user_service = UserService()

    def register(self, request: RegisterUserRequest) -> WebResponse[dict]:
        user = self.user_service.register(request)
        return WebResponse(data=user.dict(by_alias=True))