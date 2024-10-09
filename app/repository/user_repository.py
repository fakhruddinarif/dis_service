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