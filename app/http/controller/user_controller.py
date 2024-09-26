from fastapi import HTTPException
from app.service.user_service import UserService
from app.schema.user_schema import RegisterUserRequest, UserSchema
from app.schema.base_schema import WebResponse

class UserController:
    def __init__(self, user_service: UserService):
        self.user_service = user_service

    def register(self, request: RegisterUserRequest) -> WebResponse[UserSchema]:
        try:
            user = self.user_service.register(request)
            return WebResponse(data=user)
        except HTTPException as e:
            raise e
        except Exception as e:
            raise HTTPException(status_code=500, detail=e)