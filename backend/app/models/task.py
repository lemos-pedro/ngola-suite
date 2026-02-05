"""
ZENTURY - Task Model
Tarefa com responsável obrigatório
"""

from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Index
from app.models.base import Base, AuditMixin
from datetime import datetime

class Task(Base, AuditMixin):
    """
    Modelo de Tarefa
    PRINCÍPIO 1: assigned_to_id é NOT NULL
    """
    __tablename__ = "task"
    
    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey('project.id'), nullable=False, index=True)
    title = Column(String(255), nullable=False, index=True)
    description = Column(Text, nullable=True)
    
    assigned_to_id = Column(Integer, ForeignKey('user.id'), nullable=False, index=True)
    assigned_by_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    
    status = Column(String(50), default="pending", nullable=False, index=True)
    due_date = Column(DateTime, nullable=False)
    priority = Column(String(20), default="medium")
    
    __table_args__ = (
        Index('idx_project_task_status', 'project_id', 'status'),
        Index('idx_assigned_user', 'assigned_to_id'),
    )
    
    def __repr__(self):
        return f"<Task {self.title} → {self.assigned_to_id} [{self.status}]>"
