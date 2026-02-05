"""
ZENTURY - Core Module
Núcleo da aplicação: constantes, exceções, segurança, auditoria, middleware
"""

from app.core.constants import (
    UserRole,
    TaskStatus,
    DecisionStatus,
    DocumentStatus,
    AuditAction,
    PERMISSION_MATRIX,
    VALIDATION_RULES,
    MESSAGES,
)
from app.core.exceptions import (
    ZentryException,
    UnauthorizedException,
    ForbiddenException,
    TaskMissingAssigneeException,
    DecisionNotSignedException,
    DocumentNotApprovedException,
    AuditImmutableException,
)

__all__ = [
    "UserRole",
    "TaskStatus",
    "DecisionStatus",
    "DocumentStatus",
    "AuditAction",
    "PERMISSION_MATRIX",
    "VALIDATION_RULES",
    "MESSAGES",
    "ZentryException",
    "UnauthorizedException",
    "ForbiddenException",
    "TaskMissingAssigneeException",
    "DecisionNotSignedException",
    "DocumentNotApprovedException",
    "AuditImmutableException",
]