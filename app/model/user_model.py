from sqlalchemy import Column, String, Enum
from sqlalchemy.orm import Mapped, mapped_column
from app.model.base_model import BaseModel

class User(BaseModel):
    __tablename__ = "users"

    name: Mapped[str] = mapped_column(String(100), nullable=False)
    email: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String(100), nullable=False)
    phone: Mapped[str] = mapped_column(String(20), nullable=False, unique=True)
    photo: Mapped[str] = mapped_column(String(100), nullable=True)
    role: Mapped[str] = mapped_column(Enum('buyer', 'photographer'), default='buyer', nullable=False)