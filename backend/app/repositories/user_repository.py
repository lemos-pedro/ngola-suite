"""
User Repository
Queries específicas para User
"""

from sqlalchemy.orm import Session
from app.models.user import User
from app.repositories.base import BaseRepository
from typing import Optional

class UserRepository(BaseRepository[User]):
    def __init__(self, db: Session):
        super().__init__(db, User)
    
    def get_by_email(self, email: str) -> Optional[User]:
        return self.db.query(User).filter(User.email == email).first()
    
    def get_by_role(self, role: str, skip: int = 0, limit: int = 50):
        return (
            self.db.query(User)
            .filter(User.role == role)
            .offset(skip)
            .limit(limit)
            .all()
        )
    
    def get_active_users(self, skip: int = 0, limit: int = 50):
        return (
            self.db.query(User)
            .filter(User.is_active == 1)
            .offset(skip)
            .limit(limit)
            .all()
        )
