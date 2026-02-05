"""
ZENTURY - Document Model
Documento com ciclo de vida (Princípio 3)
"""

from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from app.models.base import Base, AuditMixin
from datetime import datetime

class Document(Base, AuditMixin):
    """
    Modelo de Documento
    PRINCÍPIO 3: Documento é Ativo Operacional
    Ciclo de vida: draft → in_review → approved → signed
    """
    __tablename__ = "document"
    
    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey('project.id'), nullable=False, index=True)
    
    title = Column(String(255), nullable=False, index=True)
    content = Column(Text, nullable=False)
    version = Column(Integer, default=1, nullable=False)
    
    status = Column(String(50), default="draft", nullable=False, index=True)
    
    approved_by_id = Column(Integer, ForeignKey('user.id'), nullable=True)
    approved_at = Column(DateTime, nullable=True)
    
    signed_by_id = Column(Integer, ForeignKey('user.id'), nullable=True)
    signed_at = Column(DateTime, nullable=True)
    signature_hash = Column(String(512), nullable=True)
    
    def __repr__(self):
        return f"<Document {self.title} v{self.version} [{self.status}]>"
