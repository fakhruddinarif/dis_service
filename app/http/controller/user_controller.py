from fastapi import HTTPException, Response

from app.service.user_service import UserService
from app.schema.user_schema import RegisterUserRequest, UserSchema, LoginUserRequest, TokenSchema, GetUserRequest
from app.schema.base_schema import WebResponse
from app.http.middleware.auth import AuthMiddleware

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

    def login(self, request: LoginUserRequest, response: Response) -> WebResponse[TokenSchema]:
        try:
            user = self.user_service.login(request)
            response.headers["Authorization"] = f"Bearer {user.access_token}"
            return WebResponse(data=user)
        except HTTPException as e:
            raise e
        except Exception as e:
            raise HTTPException(status_code=500, detail=e)

    def get(self, request: GetUserRequest) -> WebResponse[UserSchema]:
        try:
            user_id = AuthMiddleware.get_user(request)
            request.id = user_id
            user = self.user_service.get(request)
            return WebResponse(data=user)
        except HTTPException as e:
            raise e
        except Exception as e:
            raise HTTPException(status_code=500, detail=e)