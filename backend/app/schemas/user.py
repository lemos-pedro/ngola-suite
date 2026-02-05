"""
User Schemas
"""

from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from app.schemas.base import BaseSchema, TimestampMixin

class UserBase(BaseModel):
    email: EmailStr
    full_name: str = Field(..., min_length=1, max_length=255)
    cargo: Optional[str] = None

class UserCreate(UserBase):
    password: str = Field(..., min_length=12)

class UserUpdate(BaseModel):
    full_name: Optional[str] = None
    cargo: Optional[str] = None

class UserResponse(BaseSchema, UserBase, TimestampMixin):
    role: str
    is_active: int
    
    class Config:
        from_attributes = True
