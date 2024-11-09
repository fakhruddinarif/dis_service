from bson import ObjectId

from app.core.database import database
from app.repository.base_repository import BaseRepository
from app.schema.user_schema import ListAccountRequest


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

    def filter(self, request: ListAccountRequest):
        query = {"_id": ObjectId(request.id)}
        if request.bank is not None:
            query["accounts.bank"] = {"$regex": request.bank, "$options": "i"}
        if request.name is not None:
            query["accounts.name"] = {"$regex": request.name, "$options": "i"}
        if request.number is not None:
            query["accounts.number"] = {"$regex": request.number, "$options": "i"}
        return query

    def list(self, request: ListAccountRequest):
        query = self.filter(request)
        total = self.collection.count_documents(query)
        accounts_data = list(self.collection.find(query, {
            "accounts.bank": 1,
            "accounts.name": 1,
            "accounts.number": 1,
            "accounts.created_at": 1,
            "accounts.updated_at": 1,
            "accounts.deleted_at": 1
        }).skip((request.page - 1) * request.size).limit(request.size))
        accounts = [account["accounts"] for account in accounts_data]
        paging = {"total_item": total}
        return accounts, paging