"""
ZENTURY - Database Session
Setup de conexão e sessão
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.config import settings

# Criar engine
engine = create_engine(
    settings.database_url,
    echo=settings.database_echo,
    pool_size=settings.database_pool_size,
    pool_recycle=settings.database_pool_recycle,
)

# Criar SessionLocal
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)

def get_db():
    """Dependency para obter sessão do DB"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()