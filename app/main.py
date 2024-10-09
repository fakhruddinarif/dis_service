from fastapi import FastAPI, HTTPException

from app.core.exception_error import http_exception_handler
from app.http.route.user_route import get_user_router
from app.core.config import config
import uvicorn

from app.repository.user_repository import UserRepository
from app.schema.user_schema import RegisterUserRequest

app = FastAPI(
    title=config.app_name,
    summary="A application service for e-commerce photo platform",
)

app.add_exception_handler(HTTPException, http_exception_handler)

app.include_router(get_user_router(), prefix="/user", tags=["User"])

# @app.post("/register")
# def register(request: RegisterUserRequest):
#     user_collection = UserRepository()
#     user = user_collection.create(request)
#     data = user_collection.find_by_id(user.inserted_id)
#     data["_id"] = str(data["_id"])
#     return {"data": data}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)