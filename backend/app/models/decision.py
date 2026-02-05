"""
ZENTURY - Decision Model
Decisão assinada (Princípio 2)
"""

from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from app.models.base import Base, AuditMixin
from datetime import datetime

class Decision(Base, AuditMixin):
    """
    Modelo de Decisão
    PRINCÍPIO 2: Decisão não é Chat
    """
    __tablename__ = "decision"
    
    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey('project.id'), nullable=False, index=True)
    task_id = Column(Integer, ForeignKey('task.id'), nullable=True)
    
    title = Column(String(255), nullable=False, index=True)
    content = Column(Text, nullable=False)
    
    decision_maker_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    signed_by_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    signed_at = Column(DateTime, nullable=False, index=True)
    signature_hash = Column(String(512), nullable=False, unique=True)
    
    status = Column(String(50), default="signed", nullable=False)
    
    def __repr__(self):
        return f"<Decision {self.title[:30]}... [ASSINADA]>"
