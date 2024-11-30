# Cart API Endpoints
This document describes the API endpoints for the cart management system.

## 1. Add Photo to Cart
``` http
POST /api/cart/
```
**Request Body**
``` json
{
    "photo_id": "5f7b3b3b7b3b3b3b3b3b3b3b",
}
```
**Response**
```json
{
    "data": {
        "_id": "5f7b3b3b7b3b3b3b3b3b3b3b",
        "photo_id": [
          "5f7b3b3b7b3b3b3b3b3b3b3b",
          "5f7b3b3b7b3b3b3b3b3b3b3b"
        ],
        "user_id": "5f7b3b3b7b3b3b3b3b3b3b3b",
        "created_at": "2020-10-05T00:00:00.000Z",
        "updated_at": "2020-10-05T00:00:00.000Z",
        "deleted_at": null
    },
    "paging": null,
    "errors": null
}
```

## 2. Delete Photo from Cart
``` http
DELETE /api/cart/{id}
```
**Response**
```json
{
    "data": true,
    "paging": null,
    "errors": null
}
```