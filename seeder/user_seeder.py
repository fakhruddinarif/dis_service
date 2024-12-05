from datetime import datetime

from bson import ObjectId
from faker import Faker
from app.core.database import database
from app.core.security import get_hashed_password

user_table = database.get_collection("users")
faker = Faker()

users = [
    {
        "name": "Admin",
        "phone": "082414238948",
        "email": "admin@gmail.com",
        "password": get_hashed_password("rahasia"),
        "username": "admin",
        "photo": None,
        "role": "admin",
        "email_verified_at": None,
        "followers": [],
        "following": [],
        "accounts": [],
        "balance": 0,
        "created_at": datetime.now(),
        "updated_at": datetime.now(),
        "deleted_at": None
    },
    {
        "name": "Ahmad Faza Alfan Fashah",
        "phone": "082414238950",
        "email": "fizifufufafa@gmail.com",
        "password": get_hashed_password("rahasia"),
        "username": "fizifufufafa",
        "photo": None,
        "role": "user",
        "email_verified_at": None,
        "followers": [],
        "following": [],
        "accounts": [],
        "balance": 0,
        "created_at": datetime.now(),
        "updated_at": datetime.now(),
        "deleted_at": None
    },
    {
        "name": "Muhammad Fakhruddin Arif",
        "phone": "082414238960",
        "email": "fakhruddinarif@gmail.com",
        "password": get_hashed_password("rahasia"),
        "username": "fakhruddinarif",
        "photo": None,
        "role": "user",
        "email_verified_at": None,
        "followers": [],
        "following": [],
        "accounts": [],
        "balance": 0,
        "created_at": datetime.now(),
        "updated_at": datetime.now(),
        "deleted_at": None
    },
    {
        "name": "Najwa Azzahra",
        "phone": "082414238970",
        "email": "najwaazzahra@gmail.com",
        "password": get_hashed_password("rahasia"),
        "username": "najwaazzahra",
        "photo": None,
        "role": "user",
        "email_verified_at": None,
        "followers": [],
        "following": [],
        "accounts": [],
        "balance": 0,
        "created_at": datetime.now(),
        "updated_at": datetime.now(),
        "deleted_at": None
    },
    {
        "name": "Rizky Reza Danuarta",
        "phone": "082414238990",
        "email": "rizkyreza@gmail.com",
        "password": get_hashed_password("rahasia"),
        "username": "rizkyreza",
        "photo": None,
        "role": "user",
        "email_verified_at": None,
        "followers": [],
        "following": [],
        "accounts": [],
        "balance": 0,
        "created_at": datetime.now(),
        "updated_at": datetime.now(),
        "deleted_at": None
    }
]

banks = [
    "BANK BRI",
    "BANK BCA",
    "BANK BNI",
    "BANK MANDIRI",
]

def seed_users():
    for user in users:
        user_table.insert_one(user)

def seed_accounts():
    users = user_table.find()
    for user in users:
        accounts = []
        for bank in banks:
            account = {
                "_id": ObjectId(),
                "bank": bank,
                "name": user["name"],
                "number": str(faker.random_number(digits=10)),
                "created_at": datetime.now(),
                "updated_at": datetime.now(),
                "deleted_at": None
            }
            accounts.append(account)
        user_table.update_one({"_id": user["_id"]}, {"$set": {"accounts": accounts}})