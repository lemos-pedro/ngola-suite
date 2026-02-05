"""
Project Repository
Queries específicas para Project
"""

from sqlalchemy.orm import Session
from app.models.project import Project
from app.repositories.base import BaseRepository
from typing import Optional, List

class ProjectRepository(BaseRepository[Project]):
    def __init__(self, db: Session):
        super().__init__(db, Project)
    
    def get_active_projects(self, skip: int = 0, limit: int = 50) -> List[Project]:
        return (
            self.db.query(Project)
            .filter(Project.is_active == 1)
            .offset(skip)
            .limit(limit)
            .all()
        )
    
    def get_by_status(self, status: str, skip: int = 0, limit: int = 50):
        return (
            self.db.query(Project)
            .filter(Project.status == status)
            .offset(skip)
            .limit(limit)
            .all()
        )
    
    def get_by_name(self, name: str) -> Optional[Project]:
        return self.db.query(Project).filter(Project.name == name).first()
