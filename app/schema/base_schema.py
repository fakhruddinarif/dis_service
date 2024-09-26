from typing import Generic, TypeVar, List, Optional
from pydantic import BaseModel

T = TypeVar('T')

class PageMetadata(BaseModel):
    page: int
    size: int
    total_item: int
    total_page: int

class WebResponse(BaseModel, Generic[T]):
    data: T
    paging: Optional[PageMetadata] = None
    errors: Optional[str] = None

    class Config:
        arbitrary_types_allowed = True

class PageResponse(BaseModel, Generic[T]):
    data: Optional[List[T]] = None
    paging: Optional[PageMetadata] = None