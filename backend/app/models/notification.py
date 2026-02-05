"""
ZENTURY - Notification Model
Notificações para usuários
"""

from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Index
from app.models.base import Base, AuditMixin
from datetime import datetime

class Notification(Base, AuditMixin):
    """
    Modelo de Notificação
    Mensagens para usuários
    """
    __tablename__ = "notification"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False, index=True)
    title = Column(String(255), nullable=False)
    message = Column(Text, nullable=False)
    entity_type = Column(String(50), nullable=True)
    entity_id = Column(Integer, nullable=True)
    
    is_read = Column(Integer, default=0, nullable=False)
    read_at = Column(DateTime, nullable=True)
    
    __table_args__ = (
        Index('idx_user_notifications', 'user_id', 'is_read'),
    )
    
    def __repr__(self):
        return f"<Notification for user {self.user_id}: {self.title[:30]}>"
