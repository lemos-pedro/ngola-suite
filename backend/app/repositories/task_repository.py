"""
Task Repository
Queries específicas para Task
"""

from sqlalchemy.orm import Session
from app.models.task import Task
from app.repositories.base import BaseRepository
from typing import List

class TaskRepository(BaseRepository[Task]):
    def __init__(self, db: Session):
        super().__init__(db, Task)
    
    def get_by_project(self, project_id: int, skip: int = 0, limit: int = 50) -> List[Task]:
        return (
            self.db.query(Task)
            .filter(Task.project_id == project_id)
            .offset(skip)
            .limit(limit)
            .all()
        )
    
    def get_by_assignee(self, user_id: int, skip: int = 0, limit: int = 50):
        return (
            self.db.query(Task)
            .filter(Task.assigned_to_id == user_id)
            .offset(skip)
            .limit(limit)
            .all()
        )
    
    def get_by_status(self, status: str, skip: int = 0, limit: int = 50):
        return (
            self.db.query(Task)
            .filter(Task.status == status)
            .offset(skip)
            .limit(limit)
            .all()
        )
    
    def get_overdue_tasks(self):
        from datetime import datetime
        return (
            self.db.query(Task)
            .filter(Task.due_date < datetime.utcnow())
            .filter(Task.status != 'completed')
            .all()
        )
