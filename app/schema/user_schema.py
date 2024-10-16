from datetime import datetime
from typing import Optional, List
from pydantic import Field, SkipValidation
from bson import Decimal128
from fastapi import UploadFile
from pydantic import BaseModel

class AccountResponse(BaseModel):
    _id: str
    bank: str
    name: str
    number: str
    created_at: datetime
    updated_at: datetime
    deleted_at: Optional[datetime]

class UserResponse(BaseModel):
    _id: str
    name: str
    phone: str
    username: Optional[str]
    email: str
    photo: Optional[str]
    role: str = "user"
    email_verified_at: Optional[datetime]
    balance: float = 0.00
    accounts: Optional[List[AccountResponse]]
    created_at: datetime
    updated_at: datetime
    deleted_at: Optional[datetime]

    class Config:
        from_attributes = True
        arbitrary_types_allowed = True

class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str

class RegisterUserRequest(BaseModel):
    name: str
    email: str
    phone: str
    password: str

class LoginUserRequest(BaseModel):
    email_or_phone: str
    password: str

class GetUserRequest(BaseModel):
    id: str

class UpdateUserRequest(BaseModel):
    id: str
    name: Optional[str]
    phone: Optional[str]
    email: Optional[str]
    username: Optional[str]

class LogoutUserRequest(BaseModel):
    id: str

class ChangePasswordRequest(BaseModel):
    id: str
    old_password: str
    new_password: str
    confirm_password: str

class ChangePhotoRequest(BaseModel):
    id: str
    photo: UploadFile

class ForgetPasswordRequest(BaseModel):
    email: str

class AddAccountRequest(BaseModel):
    id: str
    bank: str
    name: str
    number: str

class GetAccountRequest(BaseModel):
    id: str
    account_id: str

class ListAccountRequest(BaseModel):
    id: str

class UpdateAccountRequest(BaseModel):
    id: str
    account_id: str
    bank: Optional[str]
    name: Optional[str]
    number: Optional[str]

class DeleteAccountRequest(BaseModel):
    id: str
    account_id: str

class WithdrawalRequest(BaseModel):
    id: str
    account_id: str
    amount: Decimal128

    class Config:
        arbitrary_types_allowed = True