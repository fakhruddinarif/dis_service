from fastapi import APIRouter, Body, File, UploadFile, HTTPException, Form
from fastapi.params import Depends
from sqlalchemy.testing import exclude
from starlette.status import HTTP_201_CREATED
from app.core.logger import logger
from app.http.controller.photo_controller import PhotoController
from app.http.middleware.auth import get_current_user
from app.schema.base_schema import WebResponse
from app.schema.photo_schema import SellPhotoResponse, AddSellPhotoRequest, AddPostPhotoRequest, PostPhotoResponse, \
    GetPhotoRequest


def get_photo_router():
    photo_router = APIRouter()
    photo_controller = PhotoController()

    @photo_router.post("/sell", response_model=WebResponse[SellPhotoResponse], status_code=HTTP_201_CREATED)
    async def add_sell_photo(request: AddSellPhotoRequest = Depends(AddSellPhotoRequest.as_form), current_user: str = Depends(get_current_user)):
        logger.info(f"Current user: {current_user}")
        await request.file.read()
        if current_user:
            request.user_id = current_user
        else:
            raise HTTPException(status_code=400, detail="Invalid user ID")
        try:
            data = AddSellPhotoRequest(**request.dict(exclude={"file"}), file=request.file)
            return photo_controller.add_sell_photo(data, request.file)
        except HTTPException as err:
            logger.error(f"Error during add sell photo: {err.detail}")
            raise HTTPException(detail=err.detail, status_code=err.status_code)

    @photo_router.post("/post", response_model=WebResponse[PostPhotoResponse], status_code=HTTP_201_CREATED)
    async def add_post_photo(request: AddPostPhotoRequest = Depends(AddPostPhotoRequest.as_form),
                             current_user: str = Depends(get_current_user)):
        await request.file.read()
        if current_user:
            request.user_id = current_user
        else:
            raise HTTPException(status_code=400, detail="Invalid user ID")
        try:
            data = AddPostPhotoRequest(**request.dict(exclude={"file"}), file=request.file)
            return photo_controller.add_post_photo(data, request.file)
        except HTTPException as err:
            logger.error(f"Error during add post photo: {err.detail}")
            raise HTTPException(detail=err.detail, status_code=err.status_code)

    @photo_router.get("/{id}", response_model=WebResponse[dict])
    async def get(id, current_user: str = Depends(get_current_user)):
        request = GetPhotoRequest(id=id, user_id=current_user)
        logger.info(f"Get photo request: {request}")
        try:
            return photo_controller.get(request)
        except HTTPException as err:
            logger.error(f"Error during get photo: {err.detail}")
            raise HTTPException(detail=err.detail, status_code=err.status_code)

    return photo_router