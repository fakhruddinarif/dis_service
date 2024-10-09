from typing import Type

from bson import ObjectId
from typing_extensions import TypeVar
from app.model.base_model import Base
from pymongo.collection import Collection

T = TypeVar("T", bound=Base)

class BaseRepository:
    def __init__(self, collection: Collection) -> None:
        self.collection = collection

    def create(self, schema: T):
        return self.collection.insert_one(schema.dict(by_alias=True))

    def update(self, schema: T):
        return self.collection.update_one({"_id": schema.id}, {"$set": schema.dict(by_alias=True)})

    def delete(self, schema: T):
        return self.collection.update_one({"_id": schema.id}, {"$set": {"deleted_at": schema.deleted_at}})

    def last_inserted_id(self):
        return self.collection.find_one(sort=[("_id", -1)])["_id"]

    def count_by_id(self, id: ObjectId):
        return self.collection.count_documents({"_id": id})

    def find_by_id(self, id: ObjectId):
        return self.collection.find_one({"_id": id})