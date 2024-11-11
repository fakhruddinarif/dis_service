from app.core.database import database
from app.repository.base_repository import BaseRepository


class FaceRepository(BaseRepository):
    def __init__(self):
        super().__init__(database.get_collection("faces"))