from datetime import datetime
from decimal import Decimal
from bson import Decimal128
from fastapi import HTTPException
from app.model.user_model import User
from app.core.security import get_hashed_password
from app.repository.user_repository import UserRepository
from app.schema.user_schema import RegisterUserRequest, UserResponse

class UserService:
    def __init__(self):
        self.user_repository = UserRepository()

    def register(self, request: RegisterUserRequest) -> UserResponse:
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

        if self.user_repository.find_by_email(request.email):
            errors["email"] = "Email already exists"
        if self.user_repository.find_by_phone(request.phone):
            errors["phone"] = "Phone already exists"

        if errors:
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
            return UserResponse(**user.dict())
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))