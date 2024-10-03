- Create
``` json
API: /api/photo/
Method: POST
Request:
Header[Autorization]: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiIsImp0aSI6IjMwZjIwZjQwZjIwZjQwZjI
{
    "id": 1,
    "photo": file,
    "name": "photo01",
    "base_price": 10000,
    "sell_price": 11000,
    "description": "blabla badw"
}

Response:
{
    "data": {
        "url": "https://is3.cloudhost.id/storage/",
        "name": "photo01",
        "base_price": 10000,
        "sell_price": 11000,
        "description": "blabla badw",
        "user_id": 1
        "created_at": "2020-01-01 00:00:00",
        "updated_at": "2020-01-01 00:00:00"
        "deleted_at": null
    }
}
```
- Update
``` json

```
- Get
``` json

```
- List
``` json

```
- Delete
``` json

```