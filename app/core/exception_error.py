from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse
from app.core.logger import logger
import json


async def http_exception_handler(request: Request, exc: HTTPException):
    logger.error(f"HTTPException: {exc.detail}")

    # Ensure the detail is JSON serializable
    detail = exc.detail
    if not isinstance(detail, (str, dict, list)):
        detail = str(detail)

    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": detail},
    )