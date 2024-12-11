from typing import Optional
from fastapi import UploadFile, Form, File
from bson import ObjectId
from pydantic import BaseModel, Field
from datetime import datetime
from app.model.withdrawal_model import WithdrawalStatus


class WithdrawalResponse(BaseModel):
    id: str = Field(ObjectId, alias="_id")
    user_id: str = Field(ObjectId, alias="user_id")
    account_id: str = Field(ObjectId, alias="account_id")
    bank: Optional[str] = None
    amount: float
    status: WithdrawalStatus
    receipt: Optional[str] = None
    note: Optional[str] = None
    created_at: Optional[datetime]
    updated_at: Optional[datetime]
    deleted_at: Optional[datetime]

    class Config:
        from_attributes = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}

class CreateWithdrawalRequest(BaseModel):
    account_id: str
    amount: float
    user_id: Optional[str] = None

class ListWithdrawalRequest(BaseModel):
    page: int = 1
    size: int = 10

class GetWithdrawalRequest(BaseModel):
    id: str
    user_id: Optional[str] = None

class UpdateWithdrawalRequest(BaseModel):
    id: str
    status: WithdrawalStatus
    user_id: Optional[str] = None
    file: Optional[UploadFile] = None
    note: Optional[str] = None
    receipt: Optional[str] = None

    @classmethod
    def as_form(
        cls,
        id: str = Form(...),
        status: WithdrawalStatus = Form(...),
        user_id: Optional[str] = Form(None),
        file: Optional[UploadFile] = File(None),
        note: Optional[str] = Form(None),
        receipt: Optional[str] = Form(None),
    ):
        return cls(id=id, status=status, user_id=user_id, file=file, note=note, receipt=receipt)