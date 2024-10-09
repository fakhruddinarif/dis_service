from fastapi import HTTPException
from app.core.logger import logger

from app.model.user_model import User
from app.core.security import get_hashed_password, verify_password, create_access_token, create_refresh_token
from app.repository.user_repository import UserRepository
from app.schema.user_schema import RegisterUserRequest, UserResponse, LoginUserRequest, TokenResponse


class UserService:
    def __init__(self):
        self.user_repository = UserRepository()

    def register(self, request: RegisterUserRequest) -> UserResponse:
        logger.info("Register request received: {}", request.dict())
        errors = {}
        required_fields = {
            "name": "Name is required",
            "email": "Email is required",
            "password": "Password is required",
            "phone": "Phone is required"
        }

        for field, error_message in required_fields.items():
            if not getattr(request, field):
                errors[field] = error_message

        if errors:
            logger.warning("Validation errors: {}", errors)
            raise HTTPException(status_code=400, detail=errors)

        if self.user_repository.find_by_email(request.email):
            errors["email"] = "Email already exists"
        if self.user_repository.find_by_phone(request.phone):
            errors["phone"] = "Phone already exists"

        if errors:
            logger.warning("Validation errors: {}", errors)
            raise HTTPException(status_code=400, detail=errors)

        try:
            password = get_hashed_password(request.password)
            data = {
                "name": request.name,
                "email": request.email,
                "phone": request.phone,
                "password": password,
            }
            user = User(**data)
            result = self.user_repository.create(user)
            user._id = str(result.inserted_id)
            logger.info("User registered successfully: {}", user.dict())
            return UserResponse(**user.dict())
        except Exception as e:
            logger.error("Error during user registration: {}", str(e))
            raise HTTPException(status_code=500, detail=str(e))

    def login(self, request: LoginUserRequest) -> TokenResponse:
        errors = {}
        logger.info(f"Login request received: {request.dict()}")
        required_fields = {
            "email_or_phone": "Email or Phone is required",
            "password": "Password is required"
        }

        for field, error_message in required_fields.items():
            if not getattr(request, field):
                errors[field] = error_message

        if errors:
            logger.warning(f"Validation errors: {errors}")
            raise HTTPException(status_code=400, detail=errors)

        user = self.user_repository.find_email_or_phone(request.email_or_phone)
        if not user or not verify_password(request.password, user["password"]):
            errors["login"] = "Email, Phone or Password is incorrect."

        if errors:
            logger.warning(f"Validation errors: {errors}")
            raise HTTPException(status_code=400, detail=errors)

        try:
            access_token = create_access_token(user["_id"])
            refresh_token = create_refresh_token(user["_id"])
            logger.info(f"User logged in successfully: %s", user)
            return TokenResponse(access_token=access_token, refresh_token=refresh_token, token_type="bearer")
        except Exception as e:
            logger.error(f"Error during user login: {str(e)}")
            raise HTTPException(status_code=500, detail=str(e))