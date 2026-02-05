"""
ZENTURY - Signature Model
Assinatura digital
"""

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from app.models.base import Base, AuditMixin
from datetime import datetime

class Signature(Base, AuditMixin):
    """
    Modelo de Assinatura
    Prova criptográfica de assinatura
    """
    __tablename__ = "signature"
    
    id = Column(Integer, primary_key=True, index=True)
    entity_type = Column(String(50), nullable=False, index=True)
    entity_id = Column(Integer, nullable=False, index=True)
    
    signed_by_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    signed_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    
    signature_hash = Column(String(512), nullable=False, unique=True, index=True)
    algorithm = Column(String(50), default="SHA256", nullable=False)
    
    def __repr__(self):
        return f"<Signature {self.entity_type}:{self.entity_id} by user {self.signed_by_id}>"
