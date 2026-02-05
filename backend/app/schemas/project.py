"""
Project Schemas
"""

from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from app.schemas.base import BaseSchema, TimestampMixin

class ProjectBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = None
    status: str = "planning"

class ProjectCreate(ProjectBase):
    pass

class ProjectResponse(BaseSchema, ProjectBase, TimestampMixin):
    is_active: int
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    
    class Config:
        from_attributes = True
