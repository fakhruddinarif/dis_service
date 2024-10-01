from typing import Type, TypeVar
from sqlalchemy.orm import Session
from app.model.base_model import BaseModel

T = TypeVar("T", bound=BaseModel)


class BaseRepository:
    def __init__(self, db: Session, model: Type[T]) -> None:
        self.db = db
        self.model = model

    def create(self, schema: T):
        return self.db.add(schema)

    def update(self, schema: T):
        return self.db.merge(schema)

    def delete(self, schema: T):
        return self.db.delete(schema)

    def last_inserted_id(self):
        return self.db.query(self.model).order_by(self.model.id.desc()).first()

    def count_by_id(self, id: str):
        return self.db.query(self.model).filter(self.model.id == id).count()

    def find_by_id(self, id: str):
        return self.db.query(self.model).filter(self.model.id == id).first()