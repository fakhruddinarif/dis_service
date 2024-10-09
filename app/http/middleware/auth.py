from fastapi.security import HTTPBearer
from fastapi import HTTPException, Request

from app.core.config import config
from app.core.security import decode_token


class JWTBearer(HTTPBearer):
    async def __call__(self, request: Request):
        credentials = await super().__call__(request)
        token = credentials.credentials
        decoded_token = decode_token(token, config.jwt_secret_key)
        if "error" in decoded_token:
            raise HTTPException(status_code=403, detail="Invalid or expired token")
        request.state.user_id = decoded_token["sub"]
        return credentials