"""
ZENTURY - Application Constants
Constantes globais que definem o comportamento do sistema.
Respeitam os 8 princípios de Zentury.
"""

from enum import Enum

# === ROLES & PERMISSIONS (Princípio 4 e 6) ===
class UserRole(str, Enum):
    """Papéis de usuário em Zentury"""
    ADMIN = "admin"
    EXECUTIVE = "executive"
    MANAGER = "manager"
    TEAM_LEAD = "team_lead"
    ANALYST = "analyst"
    VIEWER = "viewer"

class TaskStatus(str, Enum):
    """Status de uma tarefa"""
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    BLOCKED = "blocked"
    COMPLETED = "completed"
    CANCELLED = "cancelled"

class DecisionStatus(str, Enum):
    """Status de uma decisão"""
    PENDING = "pending"
    SIGNED = "signed"
    SUPERSEDED = "superseded"
    REVOKED = "revoked"

class DocumentStatus(str, Enum):
    """Status de um documento"""
    DRAFT = "draft"
    IN_REVIEW = "in_review"
    APPROVED = "approved"
    SIGNED = "signed"
    ARCHIVED = "archived"
    OBSOLETE = "obsolete"

class AuditAction(str, Enum):
    """Ações auditadas"""
    CREATE = "CREATE"
    READ = "READ"
    UPDATE = "UPDATE"
    DELETE = "DELETE"
    SIGN = "SIGN"
    APPROVE = "APPROVE"
    REJECT = "REJECT"
    LOGIN = "LOGIN"
    LOGOUT = "LOGOUT"

# === PERMISSIONS MATRIX (Princípio 4 e 6) ===
PERMISSION_MATRIX = {
    UserRole.ADMIN: [
        "create_user", "edit_user", "delete_user",
        "manage_organization", "view_audit_logs",
        "create_project", "edit_project", "delete_project",
        "manage_decisions", "sign_documents",
        "view_all_dashboards",
    ],
    UserRole.EXECUTIVE: [
        "view_all_dashboards", "create_decision",
        "sign_decision", "view_audit_logs",
    ],
    UserRole.MANAGER: [
        "create_project", "edit_project",
        "create_task", "edit_task", "assign_task",
        "view_project_dashboard", "manage_team",
    ],
    UserRole.TEAM_LEAD: [
        "create_task", "edit_task",
        "assign_task_to_team", "view_team_dashboard",
    ],
    UserRole.ANALYST: [
        "create_task", "edit_own_task",
        "view_assigned_tasks", "update_task_status",
    ],
    UserRole.VIEWER: [
        "view_all_projects", "view_all_tasks",
    ],
}

# === VALIDATION RULES (Princípio 4 e 8) ===
VALIDATION_RULES = {
    "min_password_length": 12,
    "max_task_title_length": 255,
    "max_decision_title_length": 255,
    "max_document_title_length": 255,
    "task_requires_assigned_to": True,
    "decision_requires_signature": True,
    "document_requires_approval": True,
}

# === AUDIT SETTINGS (Princípio 5) ===
AUDIT_ENABLED = True
AUDIT_FIELDS_IMMUTABLE = ["created_at", "created_by_id", "signature_hash"]
AUDIT_LOG_RETENTION_DAYS = 2555

# === SYSTEM CONSTRAINTS ===
SYSTEM_UPTIME_TARGET = 0.999
MAX_ACTIVE_SESSIONS_PER_USER = 3
SESSION_TIMEOUT_MINUTES = 30

# === RATE LIMITING ===
RATE_LIMIT_REQUESTS = 100
RATE_LIMIT_WINDOW_SECONDS = 60

# === MESSAGES (português) ===
MESSAGES = {
    "task_missing_assignee": "❌ Tarefa sem responsável é ilegal em Zentury",
    "decision_not_signed": "❌ Decisão não pode ser salva sem assinatura",
    "document_not_approved": "❌ Documento não aprovado não pode progredir",
    "insufficient_permissions": "❌ Sem permissão para realizar esta ação",
    "unauthorized": "❌ Não autenticado",
    "entity_not_found": "❌ Entidade não encontrada",
    "audit_immutable": "❌ Auditoria é imutável",
}

# === DEFAULTS ===
DEFAULT_PAGE_SIZE = 50
MAX_PAGE_SIZE = 1000
DEFAULT_SORT_FIELD = "created_at"
DEFAULT_SORT_ORDER = "desc"