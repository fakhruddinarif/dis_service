from typing import Tuple, List
from app.schema.base_schema import WebResponse
from app.schema.user_schema import RegisterUserRequest, LoginUserRequest, GetUserRequest, LogoutUserRequest, \
    UpdateUserRequest, ChangePasswordRequest, AddAccountRequest, UserResponse, ChangePhotoRequest, ListAccountRequest, \
    AccountResponse, GetAccountRequest, ForgetPasswordRequest, UpdateAccountRequest, DeleteAccountRequest, \
    WithdrawalRequest, FollowRequest
from app.service.user_service import UserService
from fastapi import UploadFile, File


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

    def change_profile(self, request: ChangePhotoRequest, file: UploadFile = File(...)) -> WebResponse[UserResponse]:
        result = self.user_service.change_profile(request, file)
        return WebResponse(data=result)

    def forget_password(self, request: ForgetPasswordRequest) -> WebResponse[bool]:
        pass

    def add_account(self, request: AddAccountRequest) -> WebResponse[AccountResponse]:
        result = self.user_service.add_account(request)
        return WebResponse(data=result)

    def get_account(self, request: GetAccountRequest) -> WebResponse[AccountResponse]:
        result = self.user_service.get_account(request)
        return WebResponse(data=result)

    def list_account(self, request: ListAccountRequest):
        accounts, total = self.user_service.list_account(request)
        return {"data": accounts, "total": total}

    def update_account(self, request: UpdateAccountRequest) -> WebResponse[AccountResponse]:
        result = self.user_service.update_account(request)
        return WebResponse(data=result)

    def delete_account(self, request: DeleteAccountRequest) -> WebResponse[bool]:
        result = self.user_service.delete_account(request)
        return WebResponse(data=result)

    def withdrawal(self, request: WithdrawalRequest) -> WebResponse[bool]:
        result = self.user_service.withdrawal(request)
        return WebResponse(data=result)

    def follow(self, request: FollowRequest) -> WebResponse[bool]:
        result = self.user_service.follow(request)
        return WebResponse(data=result)