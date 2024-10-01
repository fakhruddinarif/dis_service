from fastapi import HTTPException
from starlette.middleware.base import BaseHTTPMiddleware

from app.service.user_service import UserService


class AuthMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, user_service: UserService):
        super().__init__(app)
        self.user_service = user_service

    async def dispatch(self, request, call_next):
        auth_header = request.headers.get("Authorization")
        if not auth_header:
            raise HTTPException(status_code=401, detail="Authorization header is required")
        try:
            token = auth_header.split("Bearer ")[1]
            user_id = self.user_service.verify_token(token)
            request.state.user_id = user_id
        except HTTPException as e:
            raise HTTPException(status_code=e.status_code, detail=e.detail)

        response = await call_next(request)
        return response

    async def get_user(self, request):
        return request.state.user_id