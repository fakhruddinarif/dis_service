import math

from fastapi import APIRouter, Body, File, UploadFile, HTTPException, Form, Request
from fastapi.responses import StreamingResponse
from fastapi.params import Depends
from typing import List
from sqlalchemy.testing import exclude
from starlette.status import HTTP_201_CREATED
from app.core.logger import logger
from app.http.controller.photo_controller import PhotoController
from app.http.middleware.auth import get_current_user
from app.schema.base_schema import WebResponse
from app.schema.photo_schema import SellPhotoResponse, AddSellPhotoRequest, AddPostPhotoRequest, PostPhotoResponse, \
    GetPhotoRequest, UpdatePostPhotoRequest, UpdateSellPhotoRequest, LikePhotoPostRequest, ListPhotoRequest, \
    CollectionPhotoRequest, DeletePhotoRequest


def get_photo_router():
    photo_router = APIRouter()
    photo_controller = PhotoController()

    @photo_router.post("/sell", response_model=WebResponse[SellPhotoResponse], status_code=HTTP_201_CREATED)
    async def add_sell_photo(request: AddSellPhotoRequest = Depends(AddSellPhotoRequest.as_form), current_user: str = Depends(get_current_user)):
        logger.info(f"Current user: {current_user}")
        # await request.file.read()
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

    @photo_router.get("/", response_model=WebResponse[List[dict]])
    async def list(request: Request, current_user: str = Depends(get_current_user)):
        logger.info(f"List photo request: {request}")
        data = ListPhotoRequest()
        type = request.query_params.get("type")
        page = request.query_params.get("page", 1)
        size = request.query_params.get("size", 10)
        try:
            if current_user:
                data.user_id = current_user
            if type:
                data.type = type
            data.page = page
            data.size = size

            result = photo_controller.list(data)
            total = result["total"]
            paging = {
                "page": data.page,
                "size": data.size,
                "total_item": total,
                "total_page": int(math.ceil(total / data.size))
            }
            return WebResponse(data=result["data"], paging=paging)
        except HTTPException as err:
            logger.error(f"Error during list photo: {err.detail}")
            raise HTTPException(detail=err.detail, status_code=err.status_code)

    @photo_router.patch("/post/{id}", response_model=WebResponse[PostPhotoResponse])
    async def update_post(id, request: UpdatePostPhotoRequest = Body(...), current_user: str = Depends(get_current_user)):
        if current_user:
            request.user_id = current_user
            request.id = id
        else:
            raise HTTPException(status_code=400, detail="Invalid user ID")
        try:
            return photo_controller.update_post(request)
        except HTTPException as err:
            logger.error(f"Error during update post photo: {err.detail}")
            raise HTTPException(detail=err.detail, status_code=err.status_code)

    @photo_router.patch("/sell/{id}", response_model=WebResponse[SellPhotoResponse])
    async def update_sell(id, request: UpdateSellPhotoRequest = Body(...), current_user: str = Depends(get_current_user)):
        if current_user:
            request.user_id = current_user
            request.id = id
        else:
            raise HTTPException(status_code=400, detail="Invalid user ID")
        try:
            return photo_controller.update_sell(request)
        except HTTPException as err:
            logger.error(f"Error during update sell photo: {err.detail}")
            raise HTTPException(detail=err.detail, status_code=err.status_code)

    @photo_router.delete("/{id}", response_model=WebResponse[bool])
    async def delete(id, current_user: str = Depends(get_current_user)):
        request = DeletePhotoRequest(id=id, user_id=current_user)
        try:
            return photo_controller.delete(request)
        except HTTPException as err:
            logger.error(f"Error during delete photo: {err.detail}")
            raise HTTPException(detail=err.detail, status_code=err.status_code)

    @photo_router.post("/like/{id}", response_model=WebResponse[PostPhotoResponse])
    async def like(id, request: LikePhotoPostRequest, current_user: str = Depends(get_current_user)):
        try:
            if current_user:
                request.user_id = current_user
                request.id = id
            return photo_controller.like(request)
        except HTTPException as err:
            logger.error(f"Error during like photo: {err.detail}")
            raise HTTPException(detail=err.detail, status_code=err.status_code)

    @photo_router.get("/post/sample", response_model=WebResponse[List[dict]])
    async def sample_photos():
        try:
            return photo_controller.sample_photos()
        except HTTPException as err:
            logger.error(f"Error during sample photos: {err.detail}")
            raise HTTPException(detail=err.detail, status_code=err.status_code)

    @photo_router.get("/sell/collection", response_model=WebResponse[List[dict]])
    async def collection_photos(request: Request, current_user: str = Depends(get_current_user)):
        data = CollectionPhotoRequest()
        page = request.query_params.get("page", 1)
        size = request.query_params.get("size", 10)
        try:
            if current_user:
                data.buyer_id = current_user
            data.page = page
            data.size = size
            result = photo_controller.collection_photos(data)
            total = result["total"]
            paging = {
                "page": data.page,
                "size": data.size,
                "total_item": total,
                "total_page": int(math.ceil(total / data.size))
            }
            return WebResponse(data=result["data"], paging=paging)
        except HTTPException as err:
            logger.error(f"Error during collection photos: {err.detail}")
            raise HTTPException(detail=err.detail, status_code=err.status_code)

    @photo_router.get("/sell/findme", response_model=WebResponse[List[SellPhotoResponse]])
    async def findme(current_user: str = Depends(get_current_user)):
        try:
            return photo_controller.findme(current_user)
        except HTTPException as err:
            logger.error(f"Error during find me: {err.detail}")
            raise HTTPException(detail=err.detail, status_code=err.status_code)

    return photo_router