from datetime import datetime

from bson import ObjectId

from app.core.database import database

transaction_table = database.get_collection("transactions")

data = [
    {
        "buyer_id": ObjectId("674fad1007bd9f6fcbbc247b"),
        "details": [
            {
                "seller_id": ObjectId("674fad1007bd9f6fcbbc247c"),
                "photo_id": [
                    ObjectId("674fae46414ce2c478aaef80"),
                    ObjectId("674fae58414ce2c478aaef81"),
                ],
                "total": 2200
            }
        ],
        "date": datetime.now(),
        "total": 2200,
        "status": "pending",
        "payment": None,
        "created_at": datetime.now(),
        "updated_at": datetime.now(),
        "deleted_at": None
    },
    {
        "buyer_id": ObjectId("674fad1007bd9f6fcbbc247b"),
        "details": [
            {
                "seller_id": ObjectId("674fad1007bd9f6fcbbc247c"),
                "photo_id": [
                    ObjectId("674fae46414ce2c478aaef80"),
                    ObjectId("674fae58414ce2c478aaef81"),
                ],
                "total": 2200
            }
        ],
        "date": datetime.now(),
        "total": 2200,
        "status": "paid",
        "payment": None,
        "created_at": datetime.now(),
        "updated_at": datetime.now(),
        "deleted_at": None
    },
    {
        "buyer_id": ObjectId("674fad1007bd9f6fcbbc247b"),
        "details": [
            {
                "seller_id": ObjectId("674fad1007bd9f6fcbbc247c"),
                "photo_id": [
                    ObjectId("674fae46414ce2c478aaef80"),
                    ObjectId("674fae58414ce2c478aaef81"),
                ],
                "total": 2200
            }
        ],
        "date": datetime.now(),
        "total": 2200,
        "status": "cancelled",
        "payment": None,
        "created_at": datetime.now(),
        "updated_at": datetime.now(),
        "deleted_at": None
    }
]

def seed_transactions():
    for transaction in data:
        transaction_table.insert_one(transaction)