from anyio.abc import value
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
        return self.collection.find_one({"_id": id, "accounts._id": account_id}, {"accounts.$": 1, "_id": 0})

    def filter(self, request: ListAccountRequest):
        query = {"_id": ObjectId(request.id)}
        if request.bank:
            query.update({"accounts.bank": request.bank})
        if request.name:
            query.update({"accounts.name": request.name})
        if request.number:
            query.update({"accounts.number": request.number})
        return query

    def list(self, request: ListAccountRequest):
        query = self.filter(request)
        page = request.page if request.page else 1
        size = request.size if request.size else 10
        skip = (page - 1) * size

        accounts_cursor = self.collection.aggregate([
            {"$match": query},
            {"$unwind": "$accounts"},
            {"$skip": skip},
            {"$limit": size},
            {"$group": {"_id": "$_id", "accounts": {"$push": "$accounts"}}}
        ])
        total_pipeline = [
            {"$match": query},
            {"$unwind": "$accounts"},
            {"$group": {"_id": None, "total": {"$sum": 1}}},
            {"$project": {"_id": 0, "total": 1}}
        ]
        total_result = list(self.collection.aggregate(total_pipeline))
        total = total_result[0]["total"] if total_result else 0
        account_list = [account for user in accounts_cursor for account in user.get("accounts", [])]

        return account_list, total

    def update_account(self, id: ObjectId, account_id: ObjectId, account):
        update_fields = {f"accounts.$.{key}": value for key, value in account.items()}
        return self.collection.update_one(
            {"_id": id, "accounts._id": account_id},
            {"$set": update_fields}
        )

    def delete_account(self, id: ObjectId, account_id: ObjectId):
        return self.collection.update_one({"_id": id, "accounts._id": account_id}, {"$pull": {"accounts": {"_id": account_id}}})

    def find_following(self, id: ObjectId, target_id: ObjectId):
        return self.collection.find_one({"_id": id, "following": target_id})

    def add_following(self, id: ObjectId, target_id: ObjectId):
        return self.collection.update_many(
        {"_id": {"$in": [id, target_id]}},
        [
            {
                "$set": {
                    "following": {
                        "$cond": [{"$eq": ["$_id", id]}, {"$setUnion": ["$following", [target_id]]}, "$following"]
                    },
                    "followers": {
                        "$cond": [{"$eq": ["$_id", target_id]}, {"$setUnion": ["$followers", [id]]}, "$followers"]
                    }
                }
            }
        ]
    )

    def remove_following(self, id: ObjectId, target_id: ObjectId):
        return self.collection.update_many(
            {"_id": {"$in": [id, target_id]}},
            [
                {
                    "$set": {
                        "following": {
                            "$cond": [{"$eq": ["$_id", id]}, {"$setDifference": ["$following", [target_id]]}, "$following"]
                        },
                        "followers": {
                            "$cond": [{"$eq": ["$_id", target_id]}, {"$setDifference": ["$followers", [id]]}, "$followers"]
                        }
                    }
                }
            ]
        )