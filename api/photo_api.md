# Photo API Endpoints
This document describes the API endpoints for the photo management system.

## 1. Upload Photo Sell
``` http
POST /api/photo/sell
```
**Headers**
``` json
{
    "Authorization": "Bearer access_token",
    "Content-Type": "multipart/form-data"
}
```
**Request Body**
```
-- form-data
name: Text = Photo Name
base_price: Text = 100000
description: Text = Photo Description
file: File
sell_price: Text = 150000
```
**Response Body**
``` json
{
    "data": {
        "_id": "5f7b3b3b7b3b3b3b3b3b3b3b",
        "name": "Photo Name",
        "base_price": "100000",
        "sell_price": "150000",
        "description": "Photo Description",
        "type": "sell",
        "status": "available",
        "user_id": "5f7b3b3b7b3b3b3b3b3b3b3b",
        "embeddings": null,
        "created_at": "2021-01-01T00:00:00.000Z",
        "updated_at": "2021-01-01T00:00:00.000Z",
        "deleted_at": null
    },
    "paging": null,
    "errors": null
}
```

## 2. Upload Photo Post
``` http
POST /api/photo/post
```
**Headers**
``` json
{
    "Authorization": "Bearer access_token",
    "Content-Type": "multipart/form-data"
}
```
**Request Body**
```
-- form-data
file: File
name: Text = Photo Name
description: Text = Photo Description
```
**Response**
``` json
{
    "data": {
        "_id": "5f7b3b3b7b3b3b3b3b3b3b3b",
        "name": "Photo Name",
        "description": "Photo Description",
        "type": "post",
        "user_id": "5f7b3b3b7b3b3b3b3b3b3b3b",
        "created_at": "2021-01-01T00:00:00.000Z",
        "updated_at": "2021-01-01T00:00:00.000Z",
        "deleted_at": null
    },
    "paging": null,
    "errors": null
}
```

## 3. Get Photo
``` http
GET /api/photo/{id}
```
**Headers**
``` json
{
    "Authorization": "Bearer access_token"
}
```
**Response**
- Post Photo
``` json
{
    "data": {
        "_id": "5f7b3b3b7b3b3b3b3b3b3b3b",
        "name": "Photo Name",
        "description": "Photo Description",
        "type": "post",
        "user_id": "5f7b3b3b7b3b3b3b3b3b3b3b",
        "created_at": "2021-01-01T00:00:00.000Z",
        "updated_at": "2021-01-01T00:00:00.000Z",
        "deleted_at": null
    },
    "paging": null,
    "errors": null
}
```
- Sell Photo
``` json
{
    "data": {
        "_id": "5f7b3b3b7b3b3b3b3b3b3b3b",
        "name": "Photo Name",
        "base_price": "100000",
        "sell_price": "150000",
        "description": "Photo Description",
        "type": "sell",
        "status": "available",
        "user_id": "5f7b3b3b7b3b3b3b3b3b3b3b",
        "embeddings": null,
        "created_at": "2021-01-01T00:00:00.000Z",
        "updated_at": "2021-01-01T00:00:00.000Z",
        "deleted_at": null
    },
    "paging": null,
    "errors": null
}
```

## 4. List Photo
``` http
GET /api/photo
```
**Headers**
``` json
{
    "Authorization":"Bearer access_token"
}
```
**Query Parameters**
```
- type: Text = post/sell
- page: Number = 1
- size: Number = 10
```
**Response**
- Post Photo
``` json
{
    "data": [
        {
            "_id": "5f7b3b3b7b3b3b3b3b3b3b3b",
            "name": "Photo Name",
            "description": "Photo Description",
            "type": "post",
            "user_id": "5f7b3b3b7b3b3b3b3b3b3b3b",
            "created_at": "2021-01-01T00:00:00.000Z",
            "updated_at": "2021-01-01T00:00:00.000Z",
            "deleted_at": null
        },
        {
            "_id": "5f7b3b3b7b3b3b3b3b3b3b3b",
            "name": "Photo Name",
            "description": "Photo Description",
            "type": "post",
            "user_id": "5f7b3b3b7b3b3b3b3b3b3b3b",
            "created_at": "2021-01-01T00:00:00.000Z",
            "updated_at": "2021-01-01T00:00:00.000Z",
            "deleted_at": null
        }
    ],
    "paging": {
        "page": 1,
        "size": 10,
        "total_item": 2,
        "total_page": 1
    },
    "errors": null
}
```
- Sell Photo
``` json
{
    "data": [
        {
            "_id": "5f7b3b3b7b3b3b3b3b3b3b3b",
            "name": "Photo Name",
            "base_price": "100000",
            "sell_price": "150000",
            "description": "Photo Description",
            "type": "sell",
            "status": "available",
            "user_id": "5f7b3b3b7b3b3b3b3b3b3b3b",
            "embeddings": null,
            "created_at": "2021-01-01T00:00:00.000Z",
            "updated_at": "2021-01-01T00:00:00.000Z",
            "deleted_at": null
        },
        {
            "_id": "5f7b3b3b7b3b3b3b3b3b3b3b",
            "name": "Photo Name",
            "base_price": "100000",
            "sell_price": "150000",
            "description": "Photo Description",
            "type": "sell",
            "status": "available",
            "user_id": "5f7b3b3b7b3b3b3b3b3b3b3b",
            "embeddings": null,
            "created_at": "2021-01-01T00:00:00.000Z",
            "updated_at": "2021-01-01T00:00:00.000Z",
            "deleted_at": null
        }
    ],
    "paging": {
        "page": 1,
        "size": 10,
        "total_item": 2,
        "total_page": 1
    },
    "errors": null
}
```

## 5. Update Post Photo
``` http
PATCH /api/photo/post/{id}
```
**Headers**
``` json
{
    "Authorization": "Bearer access_token",
}
```
**Request Body**
``` json
{
    "name": "Photo Name",
    "description": "Photo Description"
}
```
**Response Body**
``` json
{
    "data": {
        "_id": "5f7b3b3b7b3b3b3b3b3b3b3b",
        "name": "Photo Name",
        "description": "Photo Description",
        "type": "post",
        "likes": 0,
        "comments": [],
        "liked": false,
        "user_id": "5f7b3b3b7b3b3b3b3b3b3b",
        "created_at": "2021-01-01T00:00:00.000Z",
        "updated_at": "2021-01-01T00:00:00.000Z",
        "deleted_at": null
    },
    "paging": null,
    "errors": null
}
```

## 6. Update Sell Photo
``` http
PATCH /api/photo/sell/{id}
```
**Headers**
``` json
{
    "Authorization": "Bearer access_token",
}
```
**Request Body**
``` json
{
    "name": "Photo Name",
    "base_price": "100000",
    "sell_price": "150000",
    "description": "Photo Description"
}
```
**Response Body**
``` json
{
    "data": {
        "_id": "5f7b3b3b7b3b3b3b3b3b3b3b",
        "name": "Photo Name",
        "base_price": "100000",
        "sell_price": "150000",
        "description": "Photo Description",
        "type": "sell",
        "status": "available",
        "user_id": "5f7b3b3b7b3b3b3b3b3b3b3b",
        "embeddings": null,
        "created_at": "2021-01-01T00:00:00.000Z",
        "updated_at": "2021-01-01T00:00:00.000Z",
        "deleted_at": null
    },
    "paging": null,
    "errors": null
}
```

## 7. Like Photo
``` http
POST /api/photo/like/{id}
```
**Headers**
``` json
{
    "Authorization": "Bearer access_token"
}
```
**Request Body**
``` json
{
    "liked": Boolean = true
}
```
**Response**
``` json
{
    "data": {
        "_id": "5f7b3b3b7b3b3b3b3b3b3b3b",
        "name": "Photo Name",
        "description": "Photo Description",
        "type": "post",
        "likes": 0,
        "comments": [],
        "liked": false,
        "user_id": "5f7b3b3b7b3b3b3b3b3b3b3b",
        "created_at": "2021-01-01T00:00:00.000Z",
        "updated_at": "2021-01-01T00:00:00.000Z",
        "deleted_at": null
    },
    "paging": null,
    "errors": null
}
```