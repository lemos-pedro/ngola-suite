"""
Pagination Schemas
"""

from pydantic import BaseModel, Field
from typing import Generic, TypeVar, Optional

T = TypeVar('T')

class PaginationParams(BaseModel):
    skip: int = Field(0, ge=0)
    limit: int = Field(50, ge=1, le=1000)
    sort_by: Optional[str] = "created_at"
    sort_order: Optional[str] = "desc"

class PaginatedResponse(BaseModel, Generic[T]):
    total: int
    skip: int
    limit: int
    items: list[T]
