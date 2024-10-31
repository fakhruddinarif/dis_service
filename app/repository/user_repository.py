from bson import ObjectId

from app.core.database import database
from app.repository.base_repository import BaseRepository

class UserRepository(BaseRepository):
    def __init__(self):
        super().__init__(database.get_collection("users"))

    def find_by_email(self, email):
        return self.collection.find_one({"email": email})

    def find_by_username(self, username):
        return self.collection.find_one({"username": username})

    def find_by_phone(self, phone):
        return self.collection.find_one({"phone": phone})

    def find_email_or_phone(self, email_or_phone):
        return self.collection.find_one({"$or": [{"email": email_or_phone}, {"phone": email_or_phone}]})

    def change_password(self, id: ObjectId, password):
        return self.collection.update_one({"_id": id}, {"$set": {"password": password}})

    def add_account(self, id: ObjectId, account):
        return self.collection.update_one({"_id": id}, {"$push": {"accounts": account}})

    def find_account_by_number(self, id: ObjectId, number: str, bank: str):
        return self.collection.find_one({"_id": id, "accounts.number": number, "accounts.bank": bank})

    def find_account_by_id(self, id: ObjectId, account_id: ObjectId):
        return self.collection.find_one({"_id": id, "accounts._id": account_id})