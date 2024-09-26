from fastapi import FastAPI, HTTPException
from app.core.fast_api import error_handler
from app.core.sqlalchemy import Base, engine
from app.http.route.user_router import user_router

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.add_exception_handler(HTTPException, error_handler)


@app.get("/")
def read_root():
    return {"message": "test"}
app.include_router(user_router, prefix="/user", tags=["users"])