"""
ZENTURY - FastAPI Application
Implementação dos 8 princípios
"""

import logging
from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager

from app.config import settings, validate_settings
from app.core.middleware import AuditMiddleware, RateLimitMiddleware, SecurityHeadersMiddleware
from app.core.exceptions import ZentryException

# Configurar logging
logging.basicConfig(
    level=settings.log_level,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

PRINCIPLES_MESSAGE = """
╔════════════════════════════════════════════════════════════════════════════╗
║                  🎯 ZENTURY / NGOLA SUITE - INICIALIZADO                   ║
║                                                                            ║
║                      OS 8 PRINCÍPIOS ESTÃO ATIVOS:                         ║
║                                                                            ║
║  1️⃣  Responsabilidade é o Centro                                           ║
║  2️⃣  Decisão não é Chat                                                    ║
║  3️⃣  Documento é Ativo Operacional                                         ║
║  4️⃣  Simplicidade com Regras Fortes                                        ║
║  5️⃣  Transparência > Velocidade                                            ║
║  6️⃣  Sistema Serve Organização                                             ║
║  7️⃣  Executivo Vê, Operacional Executa                                     ║
║  8️⃣  Se Não Está no Sistema, Não Existe                                    ║
║                                                                            ║
║                     ✅ PRONTO PARA TESTES                                   ║
║                                                                            ║
╚════════════════════════════════════════════════════════════════════════════╝
"""

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Eventos de startup/shutdown"""
    logger.info(PRINCIPLES_MESSAGE)
    validate_settings()
    logger.info(f"✅ Zentury iniciado: {settings.environment.upper()}")
    yield
    logger.info("🔌 Zentury encerrado")

# Criar app
app = FastAPI(
    title=settings.project_name,
    version=settings.project_version,
    lifespan=lifespan,
)

# === MIDDLEWARE ===
app.add_middleware(AuditMiddleware)
app.add_middleware(RateLimitMiddleware, requests=100, window_seconds=60)
app.add_middleware(SecurityHeadersMiddleware)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=settings.cors_allow_credentials,
    allow_methods=settings.cors_allow_methods,
    allow_headers=settings.cors_allow_headers,
)

# === EXCEPTION HANDLERS ===
@app.exception_handler(ZentryException)
async def zentury_exception_handler(request: Request, exc: ZentryException):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": exc.message,
            "error_code": exc.error_code,
            "details": exc.details,
        },
    )

@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    logger.error(f"❌ ERRO NÃO ESPERADO: {str(exc)}", exc_info=True)
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"error": "Erro interno do servidor"},
    )

# === ENDPOINTS ===
@app.get("/health", tags=["System"])
async def health_check():
    """Health check"""
    return {
        "status": "ok",
        "service": settings.project_name,
        "version": settings.project_version,
        "environment": settings.environment,
    }

@app.get("/", tags=["System"])
async def root():
    """Root endpoint"""
    return {
        "message": "Bem-vindo ao Zentury / Ngola Suite",
        "documentation": "/docs",
        "health_check": "/health",
        "principles": [
            "1. Responsabilidade é o Centro",
            "2. Decisão não é Chat",
            "3. Documento é Ativo Operacional",
            "4. Simplicidade com Regras Fortes",
            "5. Transparência > Velocidade",
            "6. Sistema Serve Organização",
            "7. Executivo Vê, Operacional Executa",
            "8. Se Não Está no Sistema, Não Existe",
        ],
    }

logger.info("✅ FastAPI app configurado")