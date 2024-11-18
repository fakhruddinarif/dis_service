from bson import ObjectId
from faker import Faker

from app.core.database import database
from app.core.security import get_hashed_password

user_table = database.get_collection("users")

faker = Faker()
num_user = 25
num_account = 5
limit_user = 10

def seed_users():
    for i in range(num_user):
        user = {
            "name": faker.name(),
            "phone": faker.phone_number(),
            "email": faker.email(domain="gmail.com"),
            "password": get_hashed_password("rahasia"),
            "username": faker.user_name(),
            "photo": "https://is3.cloudhost.id/dis/profile/6728103ba31c4076cb1a474d.jpg",
            "role": "user",
            "email_verified_at": None,
            "accounts": [],
            "balance": faker.random_number(digits=5),
            "created_at": faker.date_time_this_year(),
            "updated_at": faker.date_time_this_year(),
            "deleted_at": None
        }

        user_table.insert_one(user)

def seed_accounts():
    for i in range(limit_user):
        users = user_table.find().limit(limit_user)
        for user in users:
            accounts = []
            for j in range(num_account):
                account = {
                    "_id": ObjectId(),
                    "bank": faker.company(),
                    "name": faker.name(),
                    "number": str(faker.random_number(digits=10)),
                    "created_at": faker.date_time_this_year(),
                    "updated_at": faker.date_time_this_year(),
                    "deleted_at": None
                }
                accounts.append(account)
            user_table.update_one({"_id": user["_id"]}, {"$set": {"accounts": accounts}})