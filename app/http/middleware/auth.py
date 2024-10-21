from datetime import datetime, timedelta

import jwt
from fastapi import Request, HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse

from app.core.logger import logger
from app.core.config import config
from app.core.security import decode_token, create_access_token

security = HTTPBearer()

class AuthMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        response = await call_next(request)
        return response

async def get_current_user(request: Request):
    try:
        token = request.headers.get("Authorization").split(" ")[1]
        payload = decode_token(token, config.jwt_secret_key)
        logger.info(f"Payload: {payload}")
        if payload.get("error") == "Token has expired":
            refresh_token = request.cookies.get("refresh_token")
            if refresh_token:
                refresh_payload = decode_token(refresh_token, config.jwt_refresh_key)
                if refresh_payload.get("error") == "Token has expired":
                    raise HTTPException(status_code=401, detail="Unauthorized")
                else:
                    new_access_token = create_access_token(refresh_payload["sub"])
                    request.state.new_access_token = new_access_token
                    return refresh_payload["sub"]
            else:
                raise HTTPException(status_code=401, detail="Unauthorized")
        return payload["sub"]
    except Exception as e:
        logger.error(f"Error in get_current_user: {str(e)}")
        raise HTTPException(status_code=401, detail=e)

def remove_expired_token(token: str, secret_key: str) -> str:
    try:
        payload = decode_token(token, secret_key)
        new_exp = datetime.utcnow() - timedelta(minutes=3)
        payload["exp"] = new_exp
        new_token = jwt.encode(payload, secret_key, algorithm="HS256")
        return new_token
    except Exception as e:
        logger.error(f"Error in remove_expired_token: {str(e)}")
        raise HTTPException(status_code=401, detail=str(e))