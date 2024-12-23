import math
from typing import List

from fastapi import APIRouter, Body, Depends, HTTPException, Request
from starlette.status import HTTP_201_CREATED

from app.http.controller.cart_controller import CartController
from app.http.middleware.auth import get_current_user
from app.schema.base_schema import WebResponse
from app.schema.cart_schema import CartResponse, AddItemRequest, RemoveItemRequest, ListItemRequest, ListCartResponse
from app.core.logger import logger
from app.schema.photo_schema import SellPhotoResponse


def get_cart_routes():
    cart_router = APIRouter()
    cart_controller = CartController()

    @cart_router.post("/", response_model=WebResponse[CartResponse], status_code=HTTP_201_CREATED)
    async def add_item(request: AddItemRequest = Body(...), current_user: str = Depends(get_current_user)):
        logger.info(f"Add item to cart: {request}")
        try:
            if current_user:
                request.user_id = current_user
                return cart_controller.add_item(request)
        except Exception as e:
            logger.error(f"Add item to cart failed: {str(e)}")
            raise HTTPException(status_code=500, detail=str(e))

    @cart_router.delete("/{id}", response_model=WebResponse[bool])
    async def remove_item(id, current_user: str = Depends(get_current_user)):
        request = RemoveItemRequest()
        logger.info(f"Remove item from cart: {request}")
        try:
            if current_user:
                request.photo_id = id
                request.user_id = current_user
                return cart_controller.remove_item(request)
        except Exception as e:
            logger.error(f"Remove item from cart failed: {str(e)}")
            raise HTTPException(status_code=500, detail="Internal server error")

    @cart_router.get("/", response_model=WebResponse[List[ListCartResponse]])
    async def list(request: Request, current_user: str = Depends(get_current_user)):
        data = ListItemRequest()
        page = request.query_params.get("page", 1)
        size = request.query_params.get("size", 10)

        try:
            if current_user:
                data.user_id = current_user
            data.page = int(page)
            data.size = int(size)
            result = cart_controller.list(data)
            total = result["total"]
            paging = {
                "page": data.page,
                "size": data.size,
                "total_item": total,
                "total_page": int(math.ceil(total / data.size))
            }
            return WebResponse(data=result["data"], paging=paging)
        except Exception as e:
            logger.error(f"List cart failed: {str(e)}")
            raise HTTPException(status_code=500, detail="Internal server error")

    return cart_router