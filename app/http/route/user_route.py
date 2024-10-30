from bson import ObjectId
from fastapi import APIRouter, Depends, Request, HTTPException, Response
from starlette.status import HTTP_201_CREATED, HTTP_200_OK

from app.http.controller.user_controller import UserController
from app.http.middleware.auth import get_current_user
from app.schema.base_schema import WebResponse
from app.schema.user_schema import UserResponse, RegisterUserRequest, TokenResponse, LoginUserRequest, GetUserRequest, \
    LogoutUserRequest, UpdateUserRequest, ChangePasswordRequest
from fastapi import Body
from app.core.logger import logger


def get_user_router():
    user_router = APIRouter()
    user_controller = UserController()

    @user_router.post("/register", response_model=WebResponse[UserResponse], status_code=HTTP_201_CREATED)
    async def register(request: RegisterUserRequest = Body(...)):
        return user_controller.register(request)

    @user_router.post("/login", response_model=WebResponse[TokenResponse], status_code=HTTP_200_OK)
    async def login(response: Response, request: LoginUserRequest = Body(...)):
        try:
            token_response = user_controller.login(request)
            logger.info(f"Token response: {token_response}")
            token = token_response.data
            response.set_cookie(
                key="refresh_token",
                value=token["refresh_token"],
                httponly=True,
                max_age=604800,
                secure=False,  # Set to True in production
                samesite="Lax"
            )
            return token_response
        except HTTPException as e:
            logger.error(f"HTTPException during login: {e.detail}")
            raise e
        except Exception as e:
            logger.error(f"Exception during login: {str(e)}")
            raise HTTPException(status_code=500, detail="Internal Server Error")

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
    async def logout(request: Request, response: Response):
        try:
            access_token = request.headers.get("Authorization").split(" ")[1]
            refresh_token = request.cookies.get("refresh_token")

            if not refresh_token:
                raise HTTPException(status_code=400, detail="Invalid token")

            data = LogoutUserRequest(access_token=access_token, refresh_token=refresh_token)
            response.delete_cookie("refresh_token")
            return user_controller.logout(data)
        except Exception as e:
            logger.error(f"Error in logout: {str(e)}")
            raise HTTPException(status_code=400, detail="Invalid token")

    @user_router.patch("/update", response_model=WebResponse[dict], status_code=HTTP_200_OK)
    async def update(request: Request, current_user: str = Depends(get_current_user)):
        logger.info(f"Current user: {current_user}")
        if current_user:
            request.state.id = current_user
            data = UpdateUserRequest(id=request.state.id)
            return user_controller.update(data)
        else:
            raise HTTPException(status_code=400, detail="Invalid user ID")

    @user_router.patch("/change-password", response_model=WebResponse[dict], status_code=HTTP_200_OK)
    async def change_password(request: Request, current_user: str = Depends(get_current_user),
                              data: ChangePasswordRequest = Body(...)):
        logger.info(f"Current user: {current_user}")
        if current_user:
            request.state.id = current_user
            data.id = request.state.id
        else:
            raise HTTPException(status_code=400, detail="Invalid user ID")
        try:
            return user_controller.change_password(data)
        except HTTPException as err:
            logger.error(f"Error during change password: {err.detail}")
            raise HTTPException(detail=err.detail, status_code=err.status_code)

    return user_router