- Create
``` json
API: /api/transaction/
Method: POST
Request:
Header[Autorization]: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiIsImp0aSI6IjMwZjIwZjQwZjIwZjQwZjI
{
    "id": 1,
    "payment_method": "qris",
    "photo": [
        {
            "id": 1
        },
        {
            "id": 2
        },
    ],
    "total": 20000000,
    "status" "waiting payment"
}

Response:
{
    "data": {
        "payment_method": "qris",
        "photo": [
            {
                "id": 1
            },
            {
                "id": 2
            },
        ],
        "total": 20000000,
        "status" "waiting payment"
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