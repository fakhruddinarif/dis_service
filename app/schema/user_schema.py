from datetime import datetime
from typing import Optional, List

from bson import ObjectId
from pydantic import Field
from pydantic import BaseModel

class AccountResponse(BaseModel):
    id: str = Field(ObjectId, alias="_id")
    bank: Optional[str]
    name: Optional[str]
    number: Optional[str]
    created_at: Optional[datetime]
    updated_at: Optional[datetime]
    deleted_at: Optional[datetime]

    class Config:
        from_attributes = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}

class UserResponse(BaseModel):
    id: str = Field(ObjectId, alias="_id")
    name: Optional[str]
    phone: Optional[str]
    username: Optional[str]
    email: Optional[str]
    photo: Optional[str]
    role: Optional[str]
    email_verified_at: Optional[datetime]
    balance: Optional[float]
    followers: int = 0
    following: int = 0
    created_at: Optional[datetime]
    updated_at: Optional[datetime]
    deleted_at: Optional[datetime]

    class Config:
        from_attributes = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}

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
    name: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None
    username: Optional[str] = None

class LogoutUserRequest(BaseModel):
    id: Optional[str] = Field(None, description="User ID")
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
    id: Optional[str] = Field(None, description="User ID")
    bank: str
    name: str
    number: str

class GetAccountRequest(BaseModel):
    id: Optional[str] = Field(None, description="User ID")
    account_id: Optional[str] = Field(None, description="Account ID")

class ListAccountRequest(BaseModel):
    id: Optional[str] = Field(None, description="User ID")
    bank: Optional[str] = None
    name: Optional[str] = None
    number: Optional[str] = None
    page: int = 1
    size: int = 10

class UpdateAccountRequest(BaseModel):
    id: Optional[str] = Field(None, description="User ID")
    account_id: Optional[str] = Field(None, description="Account ID")
    bank: Optional[str] = None
    name: Optional[str] = None
    number: Optional[str] = None

class DeleteAccountRequest(BaseModel):
    id: Optional[str]
    account_id: Optional[str]

class WithdrawalRequest(BaseModel):
    id: Optional[str] = None
    amount: float

class FollowRequest(BaseModel):
    id: Optional[str] = None
    target_id: Optional[str] = None
    follow: bool # True to follow, False to unfollow