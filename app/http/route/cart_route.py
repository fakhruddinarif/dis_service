from fastapi import APIRouter, Body, Depends, HTTPException
from starlette.status import HTTP_201_CREATED

from app.http.controller.cart_controller import CartController
from app.http.middleware.auth import get_current_user
from app.schema.base_schema import WebResponse
from app.schema.cart_schema import CartResponse, AddItemRequest, RemoveItemRequest
from app.core.logger import logger

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
            raise HTTPException(status_code=500, detail="Internal server error")

    @cart_router.delete("/", response_model=WebResponse[bool])
    async def remove_item(request: RemoveItemRequest = Body(...), current_user: str = Depends(get_current_user)):
        logger.info(f"Remove item from cart: {request}")
        try:
            if current_user:
                request.user_id = current_user
                return cart_controller.remove_item(request)
        except Exception as e:
            logger.error(f"Remove item from cart failed: {str(e)}")
            raise HTTPException(status_code=500, detail="Internal server error")

    return cart_router