from fastapi import APIRouter, Depends, Request, HTTPException
from starlette.status import HTTP_201_CREATED, HTTP_200_OK

from app.http.controller.user_controller import UserController
from app.http.middleware.auth import get_current_user
from app.schema.base_schema import WebResponse
from app.schema.user_schema import UserResponse, RegisterUserRequest, TokenResponse, LoginUserRequest, GetUserRequest, \
    LogoutUserRequest, UpdateUserRequest
from fastapi import Body
from app.core.logger import logger


def get_user_router():
    user_router = APIRouter()
    user_controller = UserController()

    @user_router.post("/register", response_model=WebResponse[UserResponse], status_code=HTTP_201_CREATED)
    async def register(request: RegisterUserRequest = Body(...)):
        return user_controller.register(request)

    @user_router.post("/login", response_model=WebResponse[TokenResponse], status_code=HTTP_200_OK)
    async def login(request: LoginUserRequest = Body(...)):
        return user_controller.login(request)

    @user_router.get("/current", response_model=WebResponse[UserResponse], status_code=HTTP_200_OK)
    async def get(request: Request, current_user: str = Depends(get_current_user)):
        logger.info(f"Current user: {current_user}")
        if current_user:
            request.state.id = current_user
            data = GetUserRequest(id=request.state.id)
            return user_controller.get(data)
        else:
            raise HTTPException(status_code=400, detail="Invalid user ID")

    @user_router.post("/logout", response_model=WebResponse[dict], status_code=HTTP_200_OK)
    async def logout(request: Request, current_user: str = Depends(get_current_user)):
        logger.info(f"Current user: {current_user}")
        if current_user:
            request.state.id = current_user
            data = LogoutUserRequest(id=request.state.id)
            return user_controller.logout(data)
        else:
            raise HTTPException(status_code=400, detail="Invalid user ID")

    @user_router.patch("/update", response_model=WebResponse[dict], status_code=HTTP_200_OK)
    async def update(request: Request, data: UpdateUserRequest = Body(...), current_user: str = Depends(get_current_user)):
        logger.info(f"Current user: {current_user}")
        if current_user:
            request.state.id = current_user
            data.id = request.state.id
            return user_controller.update(data)
        else:
            raise HTTPException(status_code=400, detail="Invalid user ID")

    return user_router