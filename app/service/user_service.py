from datetime import datetime

from bson import ObjectId
from fastapi import HTTPException, Response, UploadFile, File
from pymongo.results import UpdateResult
from sqlalchemy.testing import exclude
from starlette.responses import JSONResponse

from app.core.config import config
from app.core.logger import logger
from app.core.s3_client import s3_client
from app.http.middleware.auth import remove_expired_token

from app.model.user_model import User
from app.core.security import get_hashed_password, verify_password, create_access_token, create_refresh_token
from app.repository.user_repository import UserRepository
from app.schema.user_schema import RegisterUserRequest, UserResponse, LoginUserRequest, TokenResponse, GetUserRequest, \
    LogoutUserRequest, UpdateUserRequest, ChangePasswordRequest, ChangePhotoRequest, ForgetPasswordRequest, \
    AddAccountRequest, GetAccountRequest, ListAccountRequest, UpdateAccountRequest, DeleteAccountRequest, \
    GetBalanceRequest, WithdrawalRequest, AccountResponse


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

            logger.info(f"User logged in successfully: {user}")
            return TokenResponse(access_token=access_token, refresh_token=refresh_token, token_type="bearer")
        except Exception as e:
            logger.error(f"Error during user login: {str(e)}")
            raise HTTPException(status_code=500, detail=str(e))

    def get(self, request: GetUserRequest) -> UserResponse:
        logger.info(f"Get user request received: {request.dict()}")
        try:
            user = self.user_repository.find_by_id(ObjectId(request.id))
            if not user:
                raise HTTPException(status_code=404, detail="User not found")
            logger.info(f"User found: {user}")
            return UserResponse(**user)
        except Exception as e:
            logger.error(f"Error during get user: {str(e)}")
            raise HTTPException(status_code=500, detail=str(e))

    def logout(self, request: LogoutUserRequest) -> dict:
        logger.info(f"Logout user request received: {request.dict()}")
        try:
            access_token = remove_expired_token(request.access_token, config.jwt_secret_key)
            refresh_token = remove_expired_token(request.refresh_token, config.jwt_refresh_key)
            if not access_token or not refresh_token:
                raise HTTPException(status_code=400, detail="Invalid token")
            response = JSONResponse({"message": "User logged out successfully"})
            response.delete_cookie("refresh_token")
            logger.info(f"User logged out successfully: {request.access_token}")
            return {"message": "User logged out successfully"}
        except Exception as e:
            logger.error(f"Error during logout user: {str(e)}")
            raise HTTPException(status_code=500, detail=str(e))

    def update(self, request: UpdateUserRequest) -> UserResponse:
        errors = {}
        logger.info(f"Update user request received: {request.dict()}")
        required_fields = {
            "id": "ID is required",
        }

        for field, error_message in required_fields.items():
            if not getattr(request, field):
                errors[field] = error_message

        if errors:
            logger.warning(f"Validation errors: {errors}")
            raise HTTPException(status_code=400, detail=errors)
        try:
            user = self.user_repository.find_by_id(ObjectId(request.id))
            if not user:
                raise HTTPException(status_code=404, detail="User not found")

            if request.email and self.user_repository.find_by_email(request.email):
                errors["email"] = "Email already exists"

            if request.phone and self.user_repository.find_by_phone(request.phone):
                errors["phone"] = "Phone already exists"

            if request.username and self.user_repository.find_by_username(request.username):
                errors["username"] = "Username already exists"

            if errors:
                logger.warning(f"Validation errors: {errors}")
                raise HTTPException(status_code=400, detail=errors)

            user = User(**user)

            update_result: UpdateResult = self.user_repository.update(user)
            if update_result.modified_count == 1 or update_result.upserted_id:
                logger.info(f"User updated successfully: {request.dict()}")
                updated_user = self.user_repository.find_by_id(ObjectId(request.id))
                return UserResponse(**updated_user)
        except Exception as e:
            logger.error(f"Error during update user: {str(e)}")
            raise HTTPException(status_code=500, detail=str(e))

    def change_password(self, request: ChangePasswordRequest) -> bool:
        logger.info(f"Change password request received: {request.dict()}")
        try:
            user = self.user_repository.find_by_id(ObjectId(request.id))
            if not user:
                raise HTTPException(status_code=404, detail="User not found")

            if not request.new_password == request.confirm_password:
                raise HTTPException(status_code=400, detail="Password and confirm password do not match.")

            if not verify_password(request.old_password, user["password"]):
                raise HTTPException(status_code=400, detail="Old password is incorrect.")

            password = get_hashed_password(request.new_password)
            self.user_repository.change_password(ObjectId(request.id), password)
            logger.info(f"Password changed successfully: {request.id}")
            return True

        except HTTPException as e:
            logger.error(f"Error during change password: {e.detail}")
            raise e
        except Exception as e:
            logger.error(f"Error during change password: {str(e)}")
            raise HTTPException(status_code=500, detail=str(e))

    def change_profile(self, request: ChangePhotoRequest, file: UploadFile) -> UserResponse:
        errors = {}
        logger.info(f"Change photo request received: {request.dict()}")
        required_fields = {
            "id": "ID is required",
            "photo": "Photo is required"
        }

        for field, error_message in required_fields.items():
            if not getattr(request, field):
                errors[field] = error_message

        if errors:
            logger.warning(f"Validation errors: {errors}")
            raise HTTPException(status_code=400, detail=errors)

        try:
            user = self.user_repository.find_by_id(ObjectId(request.id))
            if not user:
                raise HTTPException(status_code=404, detail="User not found")

            file_extension = file.filename.split(".")[-1]
            path = f"profile/{user['_id']}.{file_extension}"

            # Upload the file to S3
            file.file.seek(0)  # Ensure the file pointer is at the beginning
            s3_client.s3.upload_fileobj(file.file, config.aws_bucket, path,
                                        ExtraArgs={"ContentType": file.content_type})
            url = f"{config.aws_url}{path}"
            user["photo"] = url
            data = User(**user)
            update_result: UpdateResult = self.user_repository.update(data)
            if update_result.modified_count == 1 or update_result.upserted_id:
                logger.info(f"Photo changed successfully: {url}")
                updated_user = self.user_repository.find_by_id(ObjectId(request.id))
                return UserResponse(**updated_user)
        except Exception as e:
            logger.error(f"Error during change photo: {str(e)}")
            raise HTTPException(status_code=500, detail=str(e))

    def forget_password(self, request: ForgetPasswordRequest):
        pass

    def add_account(self, request: AddAccountRequest): # Rekening
        logger.info(f"Add account request received: {request.dict()}")
        errors = {}
        required_fields = {
            "id": "ID is required",
            "bank": "Bank is required",
            "name": "Name is required",
            "number": "Number is required"
        }

        for field, error_message in required_fields.items():
            if not getattr(request, field):
                errors[field] = error_message

        if errors:
            logger.warning(f"Validation errors: {errors}")
            raise HTTPException(status_code=400, detail=errors)

        user = self.user_repository.find_by_id(ObjectId(request.id))
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        account = self.user_repository.find_account_by_number(ObjectId(request.id), request.number, request.bank)
        if account:
            raise HTTPException(status_code=400, detail="Account already exists")

        try:
            data = request.dict(exclude={"id"})
            data["_id"] = ObjectId()
            data["created_at"] = datetime.utcnow()
            data["updated_at"] = datetime.utcnow()
            data["deleted_at"] = None
            update_result: UpdateResult = self.user_repository.add_account(ObjectId(request.id), data)
            if update_result.upserted_id or update_result.modified_count == 1:
                logger.info(f"Account added successfully: {data}")
                updated_user = self.user_repository.find_by_id(ObjectId(request.id))
                return UserResponse(**updated_user)
        except Exception as e:
            logger.error(f"Error during add account: {str(e)}")
            raise HTTPException(status_code=500, detail=str(e))

    def get_account(self, request: GetAccountRequest) -> AccountResponse:
        logger.info(f"Get account request received: {request.dict()}")
        errors = {}
        required_fields = {
            "id": "ID is required",
            "account_id": "Account ID is required"
        }

        for field, error_message in required_fields.items():
            if not getattr(request, field):
                errors[field] = error_message

        if errors:
            logger.warning(f"Validation errors: {errors}")
            raise HTTPException(status_code=400, detail=errors)

        try:
            user = self.user_repository.find_by_id(ObjectId(request.id))
            if not user:
                raise HTTPException(status_code=404, detail="User not found")

            account = self.user_repository.find_account_by_id(ObjectId(request.id), ObjectId(request.account_id))
            if not account:
                raise HTTPException(status_code=404, detail="Account not found")

            logger.info(f"Account found: {account}")
            return AccountResponse(**account)
        except Exception as e:
            logger.error(f"Error during get account: {str(e)}")
            raise HTTPException(status_code=500, detail=str(e))

    def list_account(self, request: ListAccountRequest):
        pass

    def update_account(self, request: UpdateAccountRequest):
        pass

    def delete_account(self, request: DeleteAccountRequest):
        pass

    def get_balance(self, request: GetBalanceRequest):
        pass

    def withdrawal(self, request: WithdrawalRequest):
        pass