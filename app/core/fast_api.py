from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse

async def error_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"errors": exc.detail},
    )