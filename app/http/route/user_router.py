from fastapi import APIRouter, Depends, Response
from sqlalchemy.orm import Session
from app.schema.user_schema import UserSchema, RegisterUserRequest, TokenSchema, LoginUserRequest
from app.http.controller.user_controller import UserController
from app.schema.base_schema import WebResponse
from app.service.user_service import UserService
from app.core.sqlalchemy import get_db

user_router = APIRouter()

def get_user_controller(db: Session = Depends(get_db)):
    user_service = UserService(db)
    return UserController(user_service)

@user_router.post("/register", response_model=WebResponse[UserSchema], status_code=201)
def register(request: RegisterUserRequest, user_controller: UserController = Depends(get_user_controller)):
    return user_controller.register(request)

@user_router.post("/login", response_model=WebResponse[TokenSchema], status_code=200)
def login(request: LoginUserRequest, response: Response, user_controller: UserController = Depends(get_user_controller)):
    return user_controller.login(request, response)