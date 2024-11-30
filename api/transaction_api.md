# Transaction API Endpoints
This document describes the API endpoints for the transaction management system.

## 1. Create Transaction
``` http
POST /api/transaction
```
**Request Body**
```json
{
    "details": [
      {
        "seller_id": "5f7b3b3b7b3b3b3b3b3b3b3b",
        "photo_id": [
            "5f7b3b3b7b3b3b3b3b3b3b3b",
            "5f7b3b3b7b3b3b3b3b3b3b3b"
        ],
        "total": 1000000
      }, 
      {
        "seller_id": "5f7b3b3b7b3b3b3b3b3b3b3b",
        "photo_id": [
            "5f7b3b3b7b3b3b3b3b3b3b3b",
            "5f7b3b3b7b3b3b3b3b3b3b3b"
        ],
        "total": 1000000
      }
    ],
  "total": 2000000
}
```
**Response**
```json
{
    "data": {
        "_id": "5f7b3b3b7b3b3b3b3b3b3b3b",
        "buyer_id": "5f7b3b3b7b3b3b3b3b3b3b3b",
        "details": [
          {
            "seller_id": "5f7b3b3b7b3b3b3b3b3b3b3b",
            "photo_id": [
                "5f7b3b3b7b3b3b3b3b3b3b3b",
                "5f7b3b3b7b3b3b3b3b3b3b3b"
            ],
            "total": 1000000
          },
            {
                "seller_id": "5f7b3b3b7b3b3b3b3b3b3b3b",
                "photo_id": [
                    "5f7b3b3b7b3b3b3b3b3b3b3b",
                    "5f7b3b3b7b3b3b3b3b3b3b3b"
                ],
                "total": 1000000
            }
        ],
        "date": "2020-10-05T00:00:00.000Z",
        "total": 2000000,
        "payment": {
          "_id": "5f7b3b3b7b3b3b3b3b3b3b3b",
          "status": "pending",
          "type": "qris",
          "url": "https://qris.com/5f7b3b3b7b3b3b3b3b3b3b3b",
          "expired_at": "2020-10-05T00:00:00.000Z",
        },
        "status": "pending",
        "created_at": "2020-10-05T00:00:00.000Z",
        "updated_at": "2020-10-05T00:00:00.000Z",
        "deleted_at": null
    },
    "paging": null,
    "errors": null,
}
```