"""
ZENTURY - Organization Model
Organização/Departamento
"""

from sqlalchemy import Column, Integer, String, Text
from app.models.base import Base, AuditMixin

class Organization(Base, AuditMixin):
    """
    Modelo de Organização
    Contexto para projetos e responsabilidades
    """
    __tablename__ = "organization"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), unique=True, nullable=False, index=True)
    description = Column(Text, nullable=True)
    is_active = Column(Integer, default=1, nullable=False)
    
    def __repr__(self):
        return f"<Organization {self.name}>"
