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
        try:
            if not request.name or not request.email or not request.password:
                raise HTTPException(status_code=400, detail="Invalid request")
            if self.user_repository.find_by_email(request.email):
                raise HTTPException(status_code=400, detail="Email already registered")
            password = pwd_context.hash(request.password)
            user = User(name=request.name, email=request.email, password=password, phone=request.phone)
            self.user_repository.create(user)
            self.user_repository.db.commit()
            self.user_repository.db.refresh(user)
            return UserSchema.from_orm(user)
        except HTTPException as err:
            self.user_repository.db.rollback()
            raise err
        except Exception as err:
            self.user_repository.db.rollback()
            raise HTTPException(status_code=500, detail=str(err))