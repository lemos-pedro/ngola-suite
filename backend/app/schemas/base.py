"""
Base Schemas
Modelos base para reutilização
"""

from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

class TimestampMixin(BaseModel):
    created_at: Optional[datetime] = None
    created_by_id: Optional[int] = None
    updated_at: Optional[datetime] = None
    updated_by_id: Optional[int] = None

class BaseSchema(BaseModel):
    id: Optional[int] = None
    
    class Config:
        from_attributes = True
