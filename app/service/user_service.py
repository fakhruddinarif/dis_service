import jwt
from fastapi import HTTPException
from passlib.context import CryptContext
from sqlalchemy.orm import Session

from app.core.config import config
from app.core.security import verify_password, get_hashed_password, create_access_token, create_refresh_token, \
    decode_token
from app.repository.user_repository import UserRepository
from app.schema.user_schema import RegisterUserRequest, UserSchema, LoginUserRequest, TokenSchema, GetUserRequest
from app.model.user_model import User

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class UserService:
    def __init__(self, db: Session):
        self.user_repository = UserRepository(db)

    def verify_token(self, token: str) -> str:
        try:
            payload = decode_token(token, config.jwt_secret_key)
            user_id = payload.get("sub")
            if not user_id:
                raise HTTPException(status_code=401, detail="Invalid token")
            return user_id
        except jwt.ExpiredSignatureError:
            raise HTTPException(status_code=401, detail="Token has expired")
        except jwt.InvalidTokenError:
            raise HTTPException(status_code=401, detail="Invalid token")

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
            password = get_hashed_password(request.password)
            user = User(name=request.name, email=request.email, password=password, phone=request.phone)
            self.user_repository.create(user)
            self.user_repository.db.commit()
            self.user_repository.db.refresh(user)
            return UserSchema.from_orm(user)
        except Exception as err:
            self.user_repository.db.rollback()
            raise HTTPException(status_code=500, detail=str(err))

    def login(self, request: LoginUserRequest) -> TokenSchema:
        errors = {}
        required_fields = {
            "email_or_phone": "Email or Phone is required",
            "password": "Password is required"
        }
        for field, error_message in required_fields.items():
            if not getattr(request, field):
                errors[field] = error_message
        if errors:
            raise HTTPException(status_code=400, detail=errors)
        try:
            user = self.user_repository.find_by_email_or_phone(request.email_or_phone)
            if not user:
                raise HTTPException(status_code=404, detail="Email, Phone, or Password is incorrect")
            if not verify_password(request.password, user.password):
                raise HTTPException(status_code=404, detail="Email, Phone, or Password is incorrect")
            access_token = create_access_token(user.id)
            refresh_token = create_refresh_token(user.id)
            return TokenSchema(access_token=access_token, expires_access=30, refresh_token=refresh_token, expires_refresh=60*24*7, token_type="bearer")
        except Exception as err:
            self.user_repository.db.rollback()
            raise HTTPException(status_code=500, detail=str(err))

    def get(self, request: GetUserRequest) -> UserSchema:
        try:
            user = self.user_repository.find_by_id(request.id)
            if not user:
                raise HTTPException(status_code=404, detail="User not found")
            return UserSchema.from_orm(user)
        except Exception as err:
            raise HTTPException(status_code=500, detail=str(err))