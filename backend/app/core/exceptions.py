"""
ZENTURY - Custom Exceptions
Exceções que enforçam os 8 princípios
"""

from fastapi import status
from typing import Optional, Any

class ZentryException(Exception):
    """Exceção base para Zentury"""
    
    def __init__(
        self,
        message: str,
        status_code: int = status.HTTP_500_INTERNAL_SERVER_ERROR,
        error_code: Optional[str] = None,
        details: Optional[dict[str, Any]] = None
    ):
        self.message = message
        self.status_code = status_code
        self.error_code = error_code or "INTERNAL_ERROR"
        self.details = details or {}
        super().__init__(self.message)

# === AUTHENTICATION ===
class UnauthorizedException(ZentryException):
    def __init__(self, message: str = "Não autenticado"):
        super().__init__(
            message=message,
            status_code=status.HTTP_401_UNAUTHORIZED,
            error_code="UNAUTHORIZED"
        )

class InvalidCredentialsException(ZentryException):
    def __init__(self, message: str = "Email ou senha inválidos"):
        super().__init__(
            message=message,
            status_code=status.HTTP_401_UNAUTHORIZED,
            error_code="INVALID_CREDENTIALS"
        )

class TokenExpiredException(ZentryException):
    def __init__(self):
        super().__init__(
            message="Token expirado. Por favor, faça login novamente.",
            status_code=status.HTTP_401_UNAUTHORIZED,
            error_code="TOKEN_EXPIRED"
        )

# === AUTHORIZATION ===
class ForbiddenException(ZentryException):
    def __init__(self, message: str = "Sem permissão para realizar esta ação"):
        super().__init__(
            message=message,
            status_code=status.HTTP_403_FORBIDDEN,
            error_code="FORBIDDEN"
        )

class InsufficientPermissionsException(ZentryException):
    def __init__(self, required_role: str = ""):
        message = f"Permissões insuficientes. Requerido: {required_role}"
        super().__init__(
            message=message,
            status_code=status.HTTP_403_FORBIDDEN,
            error_code="INSUFFICIENT_PERMISSIONS"
        )

# === VALIDATION ===
class ValidationException(ZentryException):
    def __init__(self, message: str, field: Optional[str] = None):
        super().__init__(
            message=message,
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            error_code="VALIDATION_ERROR",
            details={"field": field}
        )

# === PRINCÍPIO 1: RESPONSABILIDADE ===
class TaskMissingAssigneeException(ValidationException):
    def __init__(self):
        super().__init__(
            message="❌ Tarefa sem responsável é ilegal em Zentury",
            field="assigned_to_id"
        )

# === PRINCÍPIO 2: DECISÃO ===
class DecisionNotSignedException(ValidationException):
    def __init__(self):
        super().__init__(
            message="❌ Decisão deve ser assinada",
            field="signature"
        )

# === PRINCÍPIO 3: DOCUMENTO ===
class DocumentNotApprovedException(ValidationException):
    def __init__(self):
        super().__init__(
            message="❌ Documento não aprovado não pode progredir",
            field="status"
        )

# === NOT FOUND ===
class ResourceNotFoundException(ZentryException):
    def __init__(self, resource_type: str, resource_id: Any):
        super().__init__(
            message=f"{resource_type} com ID {resource_id} não encontrado",
            status_code=status.HTTP_404_NOT_FOUND,
            error_code="NOT_FOUND"
        )

class UserNotFoundException(ResourceNotFoundException):
    def __init__(self, user_id: Any):
        super().__init__("Usuário", user_id)

class TaskNotFoundException(ResourceNotFoundException):
    def __init__(self, task_id: Any):
        super().__init__("Tarefa", task_id)

class DecisionNotFoundException(ResourceNotFoundException):
    def __init__(self, decision_id: Any):
        super().__init__("Decisão", decision_id)

class DocumentNotFoundException(ResourceNotFoundException):
    def __init__(self, document_id: Any):
        super().__init__("Documento", document_id)

# === CONFLICT ===
class ConflictException(ZentryException):
    def __init__(self, message: str):
        super().__init__(
            message=message,
            status_code=status.HTTP_409_CONFLICT,
            error_code="CONFLICT"
        )

class StateConflictException(ConflictException):
    def __init__(self, current_state: str, attempted_state: str):
        super().__init__(
            message=f"Não é possível transicionar de '{current_state}' para '{attempted_state}'"
        )

# === PRINCÍPIO 5: AUDITORIA ===
class AuditImmutableException(ZentryException):
    def __init__(self):
        super().__init__(
            message="❌ Auditoria é imutável",
            status_code=status.HTTP_403_FORBIDDEN,
            error_code="AUDIT_IMMUTABLE"
        )

# === DATABASE ===
class DatabaseException(ZentryException):
    def __init__(self, message: str):
        super().__init__(
            message=f"Erro de banco de dados: {message}",
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            error_code="DATABASE_ERROR"
        )

# === BUSINESS ===
class BusinessProcessException(ZentryException):
    def __init__(self, message: str):
        super().__init__(
            message=message,
            status_code=status.HTTP_400_BAD_REQUEST,
            error_code="BUSINESS_PROCESS_ERROR"
        )