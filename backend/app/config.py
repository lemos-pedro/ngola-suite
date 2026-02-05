"""
ZENTURY - Configuration Module
Carrega variáveis de ambiente e define settings por ambiente.
Respeitando Princípio 4: Simplicidade com Regras Fortes
"""

from pydantic_settings import BaseSettings
from typing import List
import os

class Settings(BaseSettings):
    """Settings centralizadas da aplicação"""
    
    # === PROJECT INFO ===
    project_name: str = "Zentury / Ngola Suite"
    project_version: str = "1.0.0"
    api_v1_prefix: str = "/api/v1"
    
    # === DATABASE ===
    database_url: str = "postgresql://postgres:Alone7002@localhost:5432/nsuite"
    database_echo: bool = False
    database_pool_size: int = 20
    database_pool_recycle: int = 3600
    
    # === SECURITY ===
    secret_key: str = "change-this-in-production-minimum-32-chars"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    refresh_token_expire_days: int = 7
    
    # === FASTAPI ===
    debug: bool = False
    
    # === LOGGING ===
    log_level: str = "INFO"
    log_file: str = "logs/app.log"
    audit_log_file: str = "logs/audit.log"
    
    # === SMTP ===
    smtp_host: str = "smtp.gmail.com"
    smtp_port: int = 587
    smtp_user: str = ""
    smtp_password: str = ""
    smtp_from_email: str = "noreply@zentury.ao"
    smtp_from_name: str = "Zentury Notificações"
    
    # === REDIS ===
    redis_url: str = "redis://localhost:6379/0"
    
    # === CORS ===
    cors_origins: List[str] = ["http://localhost:3000", "http://localhost:8080"]
    cors_allow_credentials: bool = True
    cors_allow_methods: List[str] = ["GET", "POST", "PUT", "DELETE", "OPTIONS"]
    cors_allow_headers: List[str] = ["*"]
    
    # === ENVIRONMENT ===
    environment: str = os.getenv("ENVIRONMENT", "development")
    
    class Config:
        env_file = ".env"
        case_sensitive = False

# Singleton instance
settings = Settings()

# Validação de configuração
def validate_settings():
    """Valida configurações críticas"""
    if settings.environment == "production":
        assert settings.secret_key != "change-this-in-production-minimum-32-chars", \
            "❌ ERRO: SECRET_KEY não foi alterada para produção!"
        assert settings.database_url, \
            "❌ ERRO: DATABASE_URL não configurada"
        assert len(settings.secret_key) >= 32, \
            "❌ ERRO: SECRET_KEY deve ter mínimo 32 caracteres"
    
    print(f"✅ Configurações validadas ({settings.environment.upper()})")