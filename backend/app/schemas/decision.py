"""
Decision Schemas
"""

from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from app.schemas.base import BaseSchema, TimestampMixin

class DecisionBase(BaseModel):
    project_id: int
    task_id: Optional[int] = None
    title: str = Field(..., min_length=1, max_length=255)
    content: str = Field(..., min_length=1)
    decision_maker_id: int
    signed_by_id: int

class DecisionCreate(DecisionBase):
    pass

class DecisionResponse(BaseSchema, DecisionBase, TimestampMixin):
    signed_at: datetime
    signature_hash: str
    status: str
    
    class Config:
        from_attributes = True
