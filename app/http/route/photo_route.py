from fastapi import APIRouter, Body, File, UploadFile, HTTPException, Form
from fastapi.params import Depends
from starlette.status import HTTP_201_CREATED
from app.core.logger import logger
from app.http.controller.photo_controller import PhotoController
from app.http.middleware.auth import get_current_user
from app.schema.base_schema import WebResponse
from app.schema.photo_schema import SellPhotoResponse, AddSellPhotoRequest, AddPostPhotoRequest


def get_photo_router():
    photo_router = APIRouter()
    photo_controller = PhotoController()

    @photo_router.post("/sell", response_model=WebResponse[SellPhotoResponse], status_code=HTTP_201_CREATED)
    async def add_sell_photo(request: AddSellPhotoRequest = Depends(AddSellPhotoRequest.as_form), file: UploadFile = File(...), current_user: str = Depends(get_current_user)):
        logger.info(f"Current user: {current_user}")
        await file.read()
        if current_user:
            request.user_id = current_user
        else:
            raise HTTPException(status_code=400, detail="Invalid user ID")
        try:
            return photo_controller.add_sell_photo(request, file)
        except HTTPException as err:
            logger.error(f"Error during add sell photo: {err.detail}")
            raise HTTPException(detail=err.detail, status_code=err.status_code)

    @photo_router.post("/post", response_model=WebResponse[SellPhotoResponse], status_code=HTTP_201_CREATED)
    async def add_post_photo(request: AddPostPhotoRequest = Body(...), file: UploadFile = File(...), current_user: str = Depends(get_current_user)):
        logger.info(f"Current user: {current_user}")
        await file.read()
        if current_user:
            request.user_id = current_user
        else:
            raise HTTPException(status_code=400, detail="Invalid user ID")
        try:
            return photo_controller.add_post_photo(request, file)
        except HTTPException as err:
            logger.error(f"Error during add post photo: {err.detail}")
            raise HTTPException(detail=err.detail, status_code=err.status_code)

    return photo_router