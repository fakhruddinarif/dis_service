from sys import prefix

from fastapi import FastAPI, HTTPException
from starlette.middleware.cors import CORSMiddleware

from app.core.exception_error import http_exception_handler
from app.http.middleware.auth import AuthMiddleware
from app.http.route.cart_route import get_cart_routes
from app.http.route.photo_route import get_photo_router
from app.http.route.transaction_route import get_transaction_router
from app.http.route.user_route import get_user_router
from app.http.route.face_route import get_face_router
from app.core.config import config
import uvicorn

from app.http.route.withdrawal_route import get_withdrawal_router

app = FastAPI(
    title=config.app_name,
    summary="A application service for e-commerce photo platform",
)

origins = [
    "http://127.0.0.1:8000",
    "https://findme.my.id",
    "*"
]

@app.route("/", methods=["GET"])
def index():
    return {"message": "DIS Service is running"}

app.add_middleware(CORSMiddleware, allow_origins=origins, allow_credentials=True, allow_methods=["*"], allow_headers=["*"])

app.add_exception_handler(HTTPException, http_exception_handler)

app.include_router(get_user_router(), prefix="/api/user", tags=["User"])
app.include_router(get_photo_router(), prefix="/api/photo", tags=["Photo"])
app.include_router(get_face_router(), prefix="/api/face", tags=["Face"])
app.include_router(get_cart_routes(), prefix="/api/cart", tags=["Cart"])
app.include_router(get_transaction_router(), prefix="/api/transaction", tags=["Transaction"])
app.include_router(get_withdrawal_router(), prefix="/api/withdrawal", tags=["Withdrawal"])

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)