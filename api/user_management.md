# User Management API

- Register
``` json
API: /api/user/register
Method: POST
Request:
{
    "name": "John Doe",
    "email": "johdoe@gmail.com",
    "password": "rahasia",
    "phone": "08123456789",
}
Response:
{
    "data": {
        "id": 1,
        "name": "John Doe",
        "email": "johdoe@gmail.com",
        "phone": "08123456789",
        "username": null,
        "photo": null,
        "role": "user",
        "email_verified_at": null,
        "balance": 0,
        "rekening":[],
        "created_at": "2020-01-01 00:00:00",
        "updated_at": "2020-01-01 00:00:00"
        "deleted_at": null
    }
}
```
- Login
``` json
API: /api/user/login
Method: POST
Request:
{
    "email_or_phone": "johndoe@gmail.com",
    "password": "rahasia"
}

Response:
{
    "data": {
        "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiIsImp0aSI6IjMwZjIwZjQwZjIwZjQwZjI"
        "refresh_token": "def50200d1b3f7"
        "token_type": "Bearer",
        "expires_at": 30
    }
}
```
- Get
``` json
API: /api/user/current
Method: GET
Request:
Header[Autorization]: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiIsImp0aSI6IjMwZjIwZjQwZjIwZjQwZjI
{
    "id": 1
}

Response:
{
    "data": {
        "id": 1,
        "name": "John Doe",
        "email": "johdoe@gmail.com",
        "phone": "08123456789",
        "username": null,
        "photo": null,
    }
}
```
- Update
``` json
API: /api/user/update
Method: Patch
Request:
Header[Autorization]: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiIsImp0aSI6IjMwZjIwZjQwZjIwZjQwZjI
{
    "id": 1,
    "name": "John Doe",
    "email": "johdoe@gmail.com",
    "phone": "08123456789",
    "username": OyeeOyeee,
}

Response:
{
    "data": {
        "id": 1,
        "name": "John Doe",
        "email": "johdoe@gmail.com",
        "phone": "08123456789",
        "username": OyeeOyeee,
    }
}
```
- Logout
``` json
API: /api/user/logout
Method: POST
Request:
Header[Autorization]: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiIsImp0aSI6IjMwZjIwZjQwZjIwZjQwZjI
{
    "id": 1
}

Response:
{
    "data": true
}
```
- Change Password
``` json
API: /api/user/change_password
Method: POST
Request:
Header[Autorization]: Bearer eyJ0e
{
    "id": 1,
    "old_password": "rahasia",
    "new_password": "rahasia123",
    "confirm_password": "rahasia123"
}

Response:
{
    "data": true
}
```
- Change Photo
``` json
API: /api/user/change_photo
Method: POST
Request:
Header[Autorhization]: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiIsImp0aSI6IjMwZjIwZjQwZjIwZjQwZjI
{
    "id": 1,
    "photo": file
}

Response:
{
    "data": {
        "photo": "https://is3.cloudhost.id/storage"
    }
}
```
- Forget Password
``` json
API: /api/user/forget_password
Method: POST
Request:
{
    "email": "johndoe@gmail.com"
}

Response:
{
    "data": true
}
```
- Add Rekening
``` json
API: /api/user/rekening/add
Method: POST
Request:
Header[Autorhization]: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiIsImp0aSI6IjMwZjIwZjQwZjIwZjQwZjI
{
    "id": 1,
    "bank": "BCA",
    "name": "John Doe",
    "number": "1234567890"
}

Response:
{
    "data": {
        "id": 1,
        "name": "John Doe",
        "email": "johdoe@gmail.com",
        "phone": "08123456789",
        "username": null,
        "photo": null,
        "role": "user",
        "email_verified_at": null,
        "balance": 0,
        "rekening":[
            {
                "id": 1,
                "bank": "BCA",
                "name": "John Doe",
                "number": "1234567890"
            }
        ],
        "created_at": "2020-01-01 00:00:00",
        "updated_at": "2020-01-01 00:00:00"
        "deleted_at": null
    }
}
```
- List Rekening
``` json
API: /api/user/rekening/list
Method: GET
Request:
Header[Autorhozation]: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiIsImp0aSI6IjMwZjIwZjQwZjIwZjQwZjI
{
    "id": 1
}

Response:
{
    "data": {
        "rekening":[
            {
                "id": 1,
                "bank": "BCA",
                "name": "John Doe",
                "number": "1234567890"
                "created_at": "2020-01-01 00:00:00",
                "updated_at": "2020-01-01 00:00:00"
                "deleted_at": null
            }
        ],
    }
}
```
- Update Rekening
``` json
API: /api/user/rekening/update
Method: PATCH
Request:
Header[Autorhozation]: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiIsImp0aSI6IjMwZjIwZjQwZjIwZjQwZjI
{
    "id": 1,
    "rekening_id": 1,
    "bank": "BCA",
    "name": "John Doe",
    "number": "99999999"
}

Response:
{
    "data": {
        "rekening":[
            {
                "bank": "BCA",
                "name": "John Doe",
                "number": "99999999"
            }
        ],
    }
}
```
- Delete Rekening
``` json
API: /api/user/rekening/delete
Method: DELETE
Request:
Header[Autorhozation]: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiIsImp0aSI6IjMwZjIwZjQwZjIwZjQwZjI
{
    "id": 1,
    "rekening_id": 1
    "bank": "BCA",
    "name": "John Doe",
    "number": "99999999"
}

Response:
{
    "data": {
        "id": 1,
        "bank": "BCA",
        "name": "John Doe",
        "number": "1234567890"
        "created_at": "2020-01-01 00:00:00",
        "updated_at": "2020-01-01 00:00:00"
        "deleted_at": "2020-01-01 00:00:00"
    }
}
```
- Get Balance
``` json
API: /api/user/balance
Method: GET
Request:
Header[Autorhozation]: BeareyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiIsImp0aSI6IjMwZjIwZjQwZjIwZjQwZjI
{
    "id": 1,
}

Response:
{
    "data": {
        "balance": 100000
     }
}
```
- Penarikan
``` json
API: /api/user/penarikan
Method: POST
Request:
Header[Autorhozation]: BeareyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiIsImp0aSI6IjMwZjIwZjQwZjIwZjQwZjI
{
    "id": 1,
    "rekening_id": 1,
    "amount": 100000
}

Response:
{
    "data": {
        "balance": 100000
     }
}
```