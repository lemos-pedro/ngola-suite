"""
Base Repository
CRUD genérico para todos os models
"""

from sqlalchemy.orm import Session
from sqlalchemy import desc
from typing import TypeVar, Generic, Type, List, Optional, Any

T = TypeVar('T')

class BaseRepository(Generic[T]):
    def __init__(self, db: Session, model: Type[T]):
        self.db = db
        self.model = model
    
    def create(self, obj_in: dict) -> T:
        db_obj = self.model(**obj_in)
        self.db.add(db_obj)
        self.db.commit()
        self.db.refresh(db_obj)
        return db_obj
    
    def get(self, id: int) -> Optional[T]:
        return self.db.query(self.model).filter(self.model.id == id).first()
    
    def get_all(self, skip: int = 0, limit: int = 50) -> List[T]:
        return self.db.query(self.model).offset(skip).limit(limit).all()
    
    def update(self, id: int, obj_in: dict) -> Optional[T]:
        db_obj = self.get(id)
        if db_obj:
            for key, value in obj_in.items():
                setattr(db_obj, key, value)
            self.db.commit()
            self.db.refresh(db_obj)
        return db_obj
    
    def delete(self, id: int) -> bool:
        db_obj = self.get(id)
        if db_obj:
            self.db.delete(db_obj)
            self.db.commit()
            return True
        return False
    
    def count(self) -> int:
        return self.db.query(self.model).count()
