from fastapi import HTTPException
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from app.repository.user_repository import UserRepository
from app.schema.user_schema import RegisterUserRequest, UserSchema
from app.model.user_model import User

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class UserService:
    def __init__(self, db: Session):
        self.user_repository = UserRepository(db)

    def register(self, request: RegisterUserRequest) -> UserSchema:
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
            password = pwd_context.hash(request.password)
            user = User(name=request.name, email=request.email, password=password, phone=request.phone)
            self.user_repository.create(user)
            self.user_repository.db.commit()
            self.user_repository.db.refresh(user)
            return UserSchema.from_orm(user)
        except Exception as err:
            self.user_repository.db.rollback()
            raise HTTPException(status_code=500, detail=str(err))