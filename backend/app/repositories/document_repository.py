"""
Document Repository
Queries específicas para Document
"""

from sqlalchemy.orm import Session
from app.models.document import Document
from app.repositories.base import BaseRepository
from typing import List

class DocumentRepository(BaseRepository[Document]):
    def __init__(self, db: Session):
        super().__init__(db, Document)
    
    def get_by_project(self, project_id: int, skip: int = 0, limit: int = 50) -> List[Document]:
        return (
            self.db.query(Document)
            .filter(Document.project_id == project_id)
            .offset(skip)
            .limit(limit)
            .all()
        )
    
    def get_by_status(self, status: str, skip: int = 0, limit: int = 50):
        return (
            self.db.query(Document)
            .filter(Document.status == status)
            .offset(skip)
            .limit(limit)
            .all()
        )
    
    def get_by_version(self, project_id: int, version: int):
        return (
            self.db.query(Document)
            .filter(Document.project_id == project_id)
            .filter(Document.version == version)
            .all()
        )
