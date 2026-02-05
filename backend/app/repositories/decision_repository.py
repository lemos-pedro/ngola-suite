"""
Decision Repository
Queries específicas para Decision
"""

from sqlalchemy.orm import Session
from app.models.decision import Decision
from app.repositories.base import BaseRepository
from typing import List

class DecisionRepository(BaseRepository[Decision]):
    def __init__(self, db: Session):
        super().__init__(db, Decision)
    
    def get_by_project(self, project_id: int, skip: int = 0, limit: int = 50) -> List[Decision]:
        return (
            self.db.query(Decision)
            .filter(Decision.project_id == project_id)
            .offset(skip)
            .limit(limit)
            .all()
        )
    
    def get_by_task(self, task_id: int):
        return (
            self.db.query(Decision)
            .filter(Decision.task_id == task_id)
            .all()
        )
    
    def get_by_decision_maker(self, user_id: int, skip: int = 0, limit: int = 50):
        return (
            self.db.query(Decision)
            .filter(Decision.decision_maker_id == user_id)
            .offset(skip)
            .limit(limit)
            .all()
        )
