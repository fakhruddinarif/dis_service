from app.schema.user_schema import RegisterUserRequest
from app.service.user_service import UserService


class UserController:
    def __init__(self):
        self.user_service = UserService()

    def register(self, request: RegisterUserRequest):
        return self.user_service.register(request)