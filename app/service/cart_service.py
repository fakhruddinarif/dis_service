from bson import ObjectId
from fastapi import HTTPException
from app.model.cart_model import Cart
from app.repository.cart_repository import CartRepository
from app.repository.photo_repository import PhotoRepository
from app.schema.cart_schema import AddItemRequest, CartResponse, RemoveItemRequest
from app.core.logger import logger


class CartService:
    def __init__(self):
        self.cart_repository = CartRepository()
        self.photo_repository = PhotoRepository()

    def add_item(self, request: AddItemRequest) -> CartResponse:
        logger.info(f"Add item to cart: {request}")
        errors = {}
        required_fields = {
            "photo_id": "Photo ID is required",
            "user_id": "User ID is required"
        }
        for field, message in required_fields.items():
            if not request.get(field):
                errors[field] = message

        if errors:
            logger.error(f"Add item to cart failed: {errors}")
            raise HTTPException(status_code=400, detail=errors)

        try:
            photo = self.photo_repository.find_by_id(ObjectId(request.photo_id))
            if not photo:
                raise HTTPException(status_code=404, detail="Photo not found")

            cart = self.cart_repository.find_by_user_id(ObjectId(request.user_id))
            if not cart:
                data = {
                    "photos": [ObjectId(request.photo_id)],
                    "user_id": ObjectId(request.user_id)
                }
                cart = Cart(**data)
                result = self.cart_repository.create(cart)
                cart.id = str(result.inserted_id)
                cart.photos = [str(photo_id) for photo_id in cart.photos]
                cart.user_id = str(cart.user_id)
            else:
                if ObjectId(request.photo_id) in cart.photos:
                    raise HTTPException(status_code=400, detail="Photo already in cart")
                cart.photos.append(request.photo_id)
                self.cart_repository.update(cart)
                cart.id = str(cart.id)
                cart.photos = [str(photo_id) for photo_id in cart.photos]
                cart.user_id = str(cart.user_id)

            logger.info(f"Add item to cart success: {cart}")
            return CartResponse(**cart.dict(by_alias=True))
        except Exception as e:
            logger.error(f"Add item to cart failed: {str(e)}")
            raise HTTPException(status_code=500, detail="Internal server error")

    def remove_item(self, request: RemoveItemRequest) -> bool:
        logger.info(f"Remove item from cart: {request}")
        errors = {}
        required_fields = {
            "photo_id": "Photo ID is required",
            "user_id": "User ID is required"
        }
        for field, message in required_fields.items():
            if not request.get(field):
                errors[field] = message

        if errors:
            logger.error(f"Add item to cart failed: {errors}")
            raise HTTPException(status_code=400, detail=errors)

        try:
            cart = self.cart_repository.find_by_user_id(ObjectId(request.user_id))
            if not cart:
                raise HTTPException(status_code=404, detail="Cart not found")
            if ObjectId(request.photo_id) not in cart.photos:
                raise HTTPException(status_code=400, detail="Photo not in cart")
            cart.photos.remove(ObjectId(request.photo_id))
            self.cart_repository.update(cart)
            logger.info(f"Remove item from cart success: {request}")
            return True
        except Exception as e:
            logger.error(f"Remove item from cart failed: {str(e)}")
            raise HTTPException(status_code=500, detail="Internal server error")