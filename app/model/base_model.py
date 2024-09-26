from datetime import datetime
from sqlalchemy import DATETIME, CHAR
from sqlalchemy.ext.declarative import as_declarative, declared_attr
from sqlalchemy.orm import Mapped, mapped_column
import uuid

@as_declarative()
class BaseModel:
    id: Mapped[str]
    __name__: str

    @declared_attr
    def __tablename__(cls) -> str:
        return cls.__name__.lower()

    id: Mapped[str] = mapped_column(CHAR(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    created_at = mapped_column(DATETIME, default=datetime.utcnow)
    updated_at = mapped_column(DATETIME, default=datetime.utcnow, onupdate=datetime.utcnow)
    deleted_at = mapped_column(DATETIME, nullable=True)