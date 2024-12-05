from app.schema.base_schema import WebResponse
from app.schema.cart_schema import AddItemRequest, CartResponse, RemoveItemRequest, ListItemRequest
from app.service.cart_service import CartService


class CartController:
    def __init__(self):
        self.cart_service = CartService()

    def add_item(self, request: AddItemRequest) -> WebResponse[CartResponse]:
        result = self.cart_service.add_item(request)
        return WebResponse(data=result)

    def remove_item(self, request: RemoveItemRequest) -> WebResponse[bool]:
        result = self.cart_service.remove_item(request)
        return WebResponse(data=result)

    def list(self, request: ListItemRequest):
        carts, total = self.cart_service.list(request)
        return {"data": carts, "total": total}