"""
Task Schemas
"""

from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from app.schemas.base import BaseSchema, TimestampMixin

class TaskBase(BaseModel):
    project_id: int
    title: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = None
    assigned_to_id: int
    status: str = "pending"
    priority: str = "medium"
    due_date: datetime

class TaskCreate(TaskBase):
    assigned_by_id: int

class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[str] = None
    priority: Optional[str] = None
    due_date: Optional[datetime] = None

class TaskResponse(BaseSchema, TaskBase, TimestampMixin):
    class Config:
        from_attributes = True
