"""
ZENTURY - Base Model
AuditMixin e DeclarativeBase
"""

from sqlalchemy import Column, DateTime, String, Integer, ForeignKey, JSON, Index
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
from typing import Dict, Any

Base = declarative_base()

class AuditMixin:
    """Mixin que torna responsabilidade rastreável - Princípio 1"""
    
    created_by_id = Column(Integer, ForeignKey('user.id'), nullable=False, index=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False, index=True)
    updated_by_id = Column(Integer, ForeignKey('user.id'), nullable=True)
    updated_at = Column(DateTime, onupdate=datetime.utcnow, nullable=True)
    
    def __repr__(self):
        return (
            f"<{self.__class__.__name__} "
            f"id={getattr(self, 'id', 'N/A')} "
            f"created_by={self.created_by_id}>"
        )
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "created_by_id": self.created_by_id,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_by_id": self.updated_by_id,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }
