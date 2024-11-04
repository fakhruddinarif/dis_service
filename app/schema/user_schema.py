from datetime import datetime
from typing import Optional, List
from pydantic import Field
from bson import Decimal128
from fastapi import UploadFile, File
from pydantic import BaseModel

class AccountResponse(BaseModel):
    _id: Optional[str]
    bank: Optional[str]
    name: Optional[str]
    number: Optional[str]
    created_at: Optional[datetime]
    updated_at: Optional[datetime]
    deleted_at: Optional[datetime]

class UserResponse(BaseModel):
    _id: Optional[str]
    name: Optional[str]
    phone: Optional[str]
    username: Optional[str]
    email: Optional[str]
    photo: Optional[str]
    role: Optional[str]
    email_verified_at: Optional[datetime]
    balance: Optional[float]
    accounts: Optional[List[AccountResponse]]
    created_at: Optional[datetime]
    updated_at: Optional[datetime]
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
    id: Optional[str] = Field(None, description="User ID")
    name: Optional[str]
    phone: Optional[str]
    email: Optional[str]
    username: Optional[str]

class LogoutUserRequest(BaseModel):
    access_token: str
    refresh_token: str

class ChangePasswordRequest(BaseModel):
    id: Optional[str] = Field(None, description="User ID")
    old_password: str
    new_password: str
    confirm_password: str

class ChangePhotoRequest(BaseModel):
    id: Optional[str] = Field(None, description="User ID")
    photo: str

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

class GetBalanceRequest(BaseModel):
    id: str
    account_id: str

class WithdrawalRequest(BaseModel):
    id: str
    account_id: str
    amount: Decimal128

    class Config:
        arbitrary_types_allowed = True