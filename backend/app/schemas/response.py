"""
Response Schemas
"""

from pydantic import BaseModel
from typing import Optional, Any, Generic, TypeVar

T = TypeVar('T')

class ResponseModel(BaseModel, Generic[T]):
    success: bool
    data: Optional[T] = None
    error: Optional[str] = None
    message: Optional[str] = None
    status_code: int = 200
