from app.schema.base_schema import WebResponse
from app.schema.user_schema import RegisterUserRequest, LoginUserRequest
from app.service.user_service import UserService


class UserController:
    def __init__(self):
        self.user_service = UserService()

    def register(self, request: RegisterUserRequest) -> WebResponse[dict]:
        user = self.user_service.register(request)
        return WebResponse(data=user.dict(by_alias=True))

    def login(self, request: LoginUserRequest) -> WebResponse[dict]:
        token = self.user_service.login(request)
        return WebResponse(data=token.dict(by_alias=True))