"""
ZENTURY - AuditLog Model
Log de auditoria imutável (Princípio 5)
"""

from sqlalchemy import Column, Integer, String, JSON, DateTime, Index
from app.models.base import Base
from datetime import datetime

class AuditLog(Base):
    """
    Modelo de Auditoria
    PRINCÍPIO 5: Imutável (append-only)
    Sem UPDATE, sem DELETE
    """
    __tablename__ = "audit_log"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=False, index=True)
    action = Column(String(50), nullable=False, index=True)
    entity_type = Column(String(50), nullable=False, index=True)
    entity_id = Column(Integer, nullable=False, index=True)
    
    old_values = Column(JSON, nullable=True)
    new_values = Column(JSON, nullable=True)
    
    timestamp = Column(DateTime, default=datetime.utcnow, nullable=False, index=True)
    ip_address = Column(String(50), nullable=True)
    user_agent = Column(String(255), nullable=True)
    
    __table_args__ = (
        Index('idx_entity_audit', 'entity_type', 'entity_id'),
    )
    
    def __repr__(self):
        return f"<AuditLog {self.action} {self.entity_type}:{self.entity_id}>"
