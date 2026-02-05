"""
Document Schemas
"""

from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from app.schemas.base import BaseSchema, TimestampMixin

class DocumentBase(BaseModel):
    project_id: int
    title: str = Field(..., min_length=1, max_length=255)
    content: str = Field(..., min_length=1)
    status: str = "draft"

class DocumentCreate(DocumentBase):
    pass

class DocumentResponse(BaseSchema, DocumentBase, TimestampMixin):
    version: int
    approved_by_id: Optional[int] = None
    approved_at: Optional[datetime] = None
    signed_by_id: Optional[int] = None
    signed_at: Optional[datetime] = None
    signature_hash: Optional[str] = None
    
    class Config:
        from_attributes = True
