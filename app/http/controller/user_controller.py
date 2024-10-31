from app.schema.base_schema import WebResponse
from app.schema.user_schema import RegisterUserRequest, LoginUserRequest, GetUserRequest, LogoutUserRequest, \
    UpdateUserRequest, ChangePasswordRequest, AddAccountRequest, UserResponse
from app.service.user_service import UserService
from fastapi import Response


class UserController:
    def __init__(self):
        self.user_service = UserService()

    def register(self, request: RegisterUserRequest) -> WebResponse[dict]:
        user = self.user_service.register(request)
        return WebResponse(data=user.dict(by_alias=True))

    def login(self, request: LoginUserRequest) -> WebResponse[dict]:
        token = self.user_service.login(request)
        return WebResponse(data=token.dict(by_alias=True))

    def get(self, request: GetUserRequest) -> WebResponse[dict]:
        user = self.user_service.get(request)
        return WebResponse(data=user.dict(by_alias=True))

    def logout(self, request: LogoutUserRequest) -> WebResponse[bool]:
        result = self.user_service.logout(request)
        return WebResponse(data=result)

    def update(self, request: UpdateUserRequest) -> WebResponse[dict]:
        result = self.user_service.update(request)
        return WebResponse(data=result)

    def change_password(self, request: ChangePasswordRequest) -> WebResponse[bool]:
        result = self.user_service.change_password(request)
        return WebResponse(data=result)

    def add_account(self, request: AddAccountRequest) -> WebResponse[UserResponse]:
        result = self.user_service.add_account(request)
        return WebResponse(data=result)