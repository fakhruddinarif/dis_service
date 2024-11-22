# User API Endpoints
This document describes the API endpoints for the user management system.

## 1. Register User
``` http
POST /api/user/register
```
**Request Body**
``` json
{
    "name": "John Doe",
    "email": "johndoe@gmail.com",
    "password": "rahasia",
    "phone": "081234567890"
}
```
**Response**
``` json
{
    "data": {
        "_id": "5f7b3b3b7b3b3b3b3b3b3b3b",
        "name": "John Doe",
        "phone": "081234567890",
        "username": "johndoe",
        "email": "johndoe@gmail.com",
        "photo": null,
        "role": "user",
        "email_verified_at": null,
        "balance": 0,
        "followers": 0,
        "following": 0,
        "created_at": "2020-10-05T00:00:00.000Z",
        "updated_at": "2020-10-05T00:00:00.000Z"
        "deleted_at": null
    },
    "paging": null,
    "errors": null,
}
```

## 2. Login User
``` http
POST /api/user/login
```
**Request Body**
``` json
{
    "email_or_phone": "johndoe@gmail.com",
    "password": "rahasia"
}
```
**Response**
``` json
{
    "data": {
        "access_token": "access_token",
        "refresh_token": "refresh_token",
        "token_type": "bearer",
    },
    "paging": null,
    "errors": null,
}
```

## 3. Get User Profile
``` http
GET /api/user/current
```
**Request Header**
``` json
{
    "Authorization": "Bearer access_token",
}
```
**Response**
``` json
{
    "data": {
        "_id": "5f7b3b3b7b3b3b3b3b3b3b3b",
        "name": "John Doe",
        "phone": "081234567890",
        "username": "johndoe",
        "email": "johndoe@gmail.com",
        "photo": null,
        "role": "user",
        "email_verified_at": null,
        "balance": 0,
        "followers": 0,
        "following": 0,
        "created_at": "2020-10-05T00:00:00.000Z",
        "updated_at": "2020-10-05T00:00:00.000Z"
        "deleted_at": null
    },
    "paging": null,
    "errors": null,
}
```

## 4. Update User Profile
``` http
PATCH /api/user/update
```
**Request Header**
``` json
{
    "Authorization": "Bearer access_token",
}
```
**Request Body**
``` json
{
    "name": "John Doe",
    "phone": "081234567890",
    "username": "johndoe",
    "email": "johndoe@gmail.com",
}
```
**Response**
``` json
{
    "data": {
        "_id": "5f7b3b3b7b3b3b3b3b3b3b3b",
        "name": "John Doe",
        "phone": "081234567890",
        "username": "johndoe",
        "email": "johndoe@gmail.com",
        "photo": null,
        "role": "user",
        "email_verified_at": null,
        "balance": 0,
        "followers": 0,
        "following": 0,
        "created_at": "2020-10-05T00:00:00.000Z",
        "updated_at": "2020-10-05T00:00:00.000Z"
        "deleted_at": null
    },
    "paging": null,
    "errors": null,
}
```

## 5. Logout User
``` http
POST /api/user/logout
```
**Request Header**
``` json
{
    "Authorization": "Bearer access_token",
}
```
**Response**
``` json
{
    "data": true,
    "paging": null,
    "errors": null,
}
```

## 6. Change Password
``` http
PATCH /api/user/change-password
```
**Request Header**
``` json
{
    "Authorization": "Bearer access_token",
}
```
**Request Body**
``` json
{
    "old_password": "rahasia",
    "new_password": "rahasia_baru",
    "confirm_password": "rahasia_baru"
}
```
**Response**
``` json
{
    "data": true,
    "paging": null,
    "errors": null,
}
```

## 7. Change Profile Picture
``` http
PATCH /api/user/change_profile
```
**Request Header**
``` json
{
    "Authorization": "Bearer access_token",
    "Content-Type": "multipart/form-data"
}
```
**Request Data**
```
-- form-data
file: file
```
**Response**
``` json
{
    "data": {
        "_id": "5f7b3b3b7b3b3b3b3b3b3b3b",
        "name": "John Doe",
        "phone": "081234567890",
        "username": "johndoe",
        "email": "johndoe@gmail.com",
        "photo": "url_photo",
        "role": "user",
        "email_verified_at": null,
        "balance": 0,
        "followers": 0,
        "following": 0,
        "created_at": "2020-10-05T00:00:00.000Z",
        "updated_at": "2020-10-05T00:00:00.000Z"
        "deleted_at": null
    },
    "paging": null,
    "errors": null,
}
```

## 8. Add Bank Account
``` http
POST /api/user/add_account
```
**Request Header**
``` json
{
    "Authorization": "Bearer access_token",
}
```
**Request Body**
``` json
{
    "bank": "BCA",
    "number": "1234567890",
    "name": "John Doe"
}
```
**Response**
``` json
{
    "data": {
        "_id": "5f7b3b3b7b3b3b3b3b3b3b3b",
        "bank": "BCA",
        "number": "1234567890",
        "name": "John Doe",
        "created_at": "2020-10-05T00:00:00.000Z",
        "updated_at": "2020-10-05T00:00:00.000Z"
        "deleted_at": null
    },
    "paging": null,
    "errors": null,
}
```

## 9. Get Bank Account
``` http
GET /api/user/account/{5f7b3b3b7b3b3b3b3b3b3b3b OR id}
```
**Request Header**
``` json
{
    "Authorization": "Bearer access_token",
}
```
**Response**
``` json
{
    "data": {
        "_id": "5f7b3b3b7b3b3b3b3b3b3b3b",
        "bank": "BCA",
        "number": "1234567890",
        "name": "John Doe",
        "created_at": "2020-10-05T00:00:00.000Z",
        "updated_at": "2020-10-05T00:00:00.000Z"
        "deleted_at": null
    },
    "paging": null,
    "errors": null,
}
```

## 10. List Bank Account
``` http
GET /api/user/accounts
```
**Request Header**
``` json
{
    "Authorization": "Bearer access_token",
}
```
**Response**
``` json
{
    "data": [
        {
            "_id": "5f7b3b3b7b3b3b3b3b3b3b3b",
            "bank": "BCA",
            "number": "1234567890",
            "name": "John Doe",
            "created_at": "2020-10-05T00:00:00.000Z",
            "updated_at": "2020-10-05T00:00:00.000Z"
            "deleted_at": null
        },
        {
            "_id": "5f7b3b3b7b3b3b3b3b3b3b3b",
            "bank": "BRI",
            "number": "1234567890",
            "name": "John Doe",
            "created_at": "2020-10-05T00:00:00.000Z",
            "updated_at": "2020-10-05T00:00:00.000Z"
            "deleted_at": null
        }
    ],
    "paging": {
        "page": 1,
        "size": 10,
        "total_item": 2,
        "total_page": 1
    },
    "errors": null,
}
```

## 11. Update Bank Account
``` http
PATCH /api/user/update_account/{5f7b3b3b7b3b3b3b3b3b3b OR id}
```
**Request Header**
``` json
{
    "Authorization": "Bearer access_token",
}
```
**Request Body**
``` json
{
    "bank": "BCA",
    "number": "1234567890",
    "name": "John Doe"
}
```
**Response**
``` json
{
    "data": {
        "_id": "5f7b3b3b7b3b3b3b3b3b3b",
        "bank": "BCA",
        "number": "1234567890",
        "name": "John Doe",
        "created_at": "2020-10-05T00:00:00.000Z",
        "updated_at": "2020-10-05T00:00:00.000Z"
        "deleted_at": null
    },
    "paging": null,
    "errors": null,
}
```

## 12. Delete Bank Account
``` http
DELETE /api/user/delete_account/{5f7b3b3b7b3b3b3b3b3b3b OR id}
```
**Request Header**
``` json
{
    "Authorization": "Bearer access_token",
}
```
**Response**
``` json
{
    "data": true,
    "paging": null,
    "errors": null,
}
```

## 13. Follow User
``` http
POST /api/user/follow/{5f7b3b3b7b3b3b3b3b3b3b OR target_id}
```
**Request Header**
``` json
{
    "Authorization": "Bearer access_token",
}
```
**Response**
``` json
{
    "data": true,
    "paging": null,
    "errors": null,
}
```