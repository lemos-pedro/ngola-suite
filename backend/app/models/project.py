"""
ZENTURY - Project Model
Projeto de trabalho
"""

from sqlalchemy import Column, Integer, String, Text, DateTime
from app.models.base import Base, AuditMixin
from datetime import datetime

class Project(Base, AuditMixin):
    """
    Modelo de Projeto
    Contexto para tarefas, decisões e documentos
    """
    __tablename__ = "project"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False, index=True)
    description = Column(Text, nullable=True)
    status = Column(String(50), default="planning", nullable=False)
    start_date = Column(DateTime, nullable=True)
    end_date = Column(DateTime, nullable=True)
    is_active = Column(Integer, default=1, nullable=False)
    
    def __repr__(self):
        return f"<Project {self.name} status={self.status}>"
