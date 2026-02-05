"""
ZENTURY - User Model
Usuários do sistema com roles
"""

from sqlalchemy import Column, Integer, String
from app.models.base import Base, AuditMixin

class User(Base, AuditMixin):
    """
    Modelo de Usuário
    Respeitando Princípio 1: Responsabilidade
    """
    __tablename__ = "user"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, nullable=False, index=True)
    full_name = Column(String(255), nullable=False)
    hashed_password = Column(String(255), nullable=False)
    role = Column(String(50), nullable=False, default="analyst")
    cargo = Column(String(255), nullable=True)
    is_active = Column(Integer, default=1, nullable=False)
    
    def __repr__(self):
        return f"<User {self.email} role={self.role}>"
