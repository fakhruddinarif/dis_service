from fastapi import FastAPI, HTTPException

from app.core.exception_error import http_exception_handler
from app.http.middleware.auth import AuthMiddleware
from app.http.route.photo_route import get_photo_router
from app.http.route.user_route import get_user_router
from app.http.route.face_route import get_face_router
from app.core.config import config
import uvicorn

from app.repository.user_repository import UserRepository
from app.schema.user_schema import RegisterUserRequest

app = FastAPI(
    title=config.app_name,
    summary="A application service for e-commerce photo platform",
)

app.add_exception_handler(HTTPException, http_exception_handler)

app.include_router(get_user_router(), prefix="/api/user", tags=["User"])
app.include_router(get_photo_router(), prefix="/api/photo", tags=["Photo"])
app.include_router(get_face_router(), prefix="/api/face", tags=["Face"])

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)