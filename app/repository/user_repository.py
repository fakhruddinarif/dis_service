from app.repository.base_repository import BaseRepository
from app.model.user_model import User

class UserRepository(BaseRepository):
    def __init__(self, db):
        super().__init__(db, User)

    def find_by_email(self, email):
        return self.db.query(self.model).filter(self.model.email == email).first()

    def find_by_phone(self, phone):
        return self.db.query(self.model).filter(self.model.phone == phone).first()