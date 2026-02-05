# ZENTURY / NGOLA SUITE - BACKEND STRUCTURE (PRODUÇÃO)

```
zentury-backend/
│
├── README.md                          # Overview do projeto
├── .env.example                       # Variáveis de ambiente (template)
├── .gitignore                         # Exclusões Git
├── docker-compose.yml                 # Orquestração local (PostgreSQL, Redis, etc)
├── Dockerfile                         # Imagem para produção
├── requirements.txt                   # Dependências Python
├── pyproject.toml                     # Configuração moderna Python
│
├── app/
│   ├── __init__.py                    # Inicialização da aplicação FastAPI
│   ├── main.py                        # Ponto de entrada (FastAPI instance)
│   ├── config.py                      # Configurações (dev/prod/test)
│   │
│   ├── core/                          # Núcleo da aplicação (não muda)
│   │   ├── __init__.py
│   │   ├── constants.py               # Constantes globais (roles, status, etc)
│   │   ├── exceptions.py              # Exceções customizadas
│   │   ├── security.py                # JWT, OAuth2, hashing
│   │   ├── audit.py                   # Logger de auditoria (Princípio 1)
│   │   └── middleware.py              # Middleware de rastreabilidade
│   │
│   ├── models/                        # Modelos SQLAlchemy (Database)
│   │   ├── __init__.py
│   │   ├── base.py                    # Base model com timestamps, audit fields
│   │   ├── user.py                    # Usuário, cargo, permissões
│   │   ├── organization.py            # Empresa/Departamento
│   │   ├── project.py                 # Projeto (contexto obrigatório)
│   │   ├── task.py                    # Tarefa com responsável obrigatório
│   │   ├── decision.py                # Decisão (Princípio 2 - tipo próprio)
│   │   ├── document.py                # Documento com ciclo de vida (Princípio 3)
│   │   ├── audit_log.py               # Trilha de auditoria imutável
│   │   ├── signature.py               # Assinatura digital
│   │   └── notification.py            # Sistema de notificações
│   │
│   ├── schemas/                       # Pydantic schemas (validação + serialização)
│   │   ├── __init__.py
│   │   ├── base.py                    # Base schema com audit fields
│   │   ├── user.py                    # UserCreate, UserUpdate, UserResponse
│   │   ├── project.py                 # ProjectCreate, ProjectResponse
│   │   ├── task.py                    # TaskCreate, TaskUpdate, TaskResponse
│   │   ├── decision.py                # DecisionCreate, DecisionResponse
│   │   ├── document.py                # DocumentCreate, DocumentResponse
│   │   └── pagination.py              # Paginação standard
│   │
│   ├── repositories/                  # Data Access Layer (DAO pattern)
│   │   ├── __init__.py
│   │   ├── base.py                    # BaseRepository (CRUD genérico)
│   │   ├── user_repository.py         # UserRepository
│   │   ├── project_repository.py      # ProjectRepository
│   │   ├── task_repository.py         # TaskRepository
│   │   ├── decision_repository.py     # DecisionRepository
│   │   └── document_repository.py     # DocumentRepository
│   │
│   ├── services/                      # Business Logic Layer
│   │   ├── __init__.py
│   │   ├── auth_service.py            # Autenticação, JWT, refresh tokens
│   │   ├── user_service.py            # Gestão de usuários
│   │   ├── organization_service.py    # Gestão de organização/departamentos
│   │   ├── project_service.py         # Gestão de projetos
│   │   ├── task_service.py            # Gestão de tarefas (responsável obrigatório)
│   │   ├── decision_service.py        # Criação de decisões (Princípio 2)
│   │   ├── document_service.py        # Ciclo de vida de documentos (Princípio 3)
│   │   ├── audit_service.py           # Trilha de auditoria
│   │   ├── notification_service.py    # Envio de notificações
│   │   ├── dashboard_service.py       # Dashboards (Executivo vs Operacional)
│   │   └── permission_service.py      # Verificação de permissões
│   │
│   ├── api/                           # API Routes (HTTP endpoints)
│   │   ├── __init__.py
│   │   ├── v1/                        # API v1
│   │   │   ├── __init__.py
│   │   │   ├── router.py              # Router principal v1
│   │   │   ├── auth/
│   │   │   │   ├── __init__.py
│   │   │   │   └── routes.py          # POST /login, /refresh, /logout
│   │   │   ├── users/
│   │   │   │   ├── __init__.py
│   │   │   │   └── routes.py          # GET/POST/PUT users
│   │   │   ├── projects/
│   │   │   │   ├── __init__.py
│   │   │   │   └── routes.py          # GET/POST/PUT projects
│   │   │   ├── tasks/
│   │   │   │   ├── __init__.py
│   │   │   │   └── routes.py          # GET/POST/PUT/DELETE tasks
│   │   │   ├── decisions/
│   │   │   │   ├── __init__.py
│   │   │   │   └── routes.py          # POST decisions (assinada)
│   │   │   ├── documents/
│   │   │   │   ├── __init__.py
│   │   │   │   └── routes.py          # GET/POST/PUT documents
│   │   │   ├── audit/
│   │   │   │   ├── __init__.py
│   │   │   │   └── routes.py          # GET audit logs (executivo)
│   │   │   └── dashboards/
│   │   │       ├── __init__.py
│   │   │       └── routes.py          # GET dashboard/executive, /operational
│   │   │
│   │   └── v2/                        # API v2 (futuro)
│   │       └── (estrutura similar)
│   │
│   ├── dependencies/                  # Injeção de dependências (FastAPI)
│   │   ├── __init__.py
│   │   ├── auth.py                    # CurrentUser, RoleRequired, etc
│   │   └── database.py                # Session database
│   │
│   ├── utils/                         # Utilidades
│   │   ├── __init__.py
│   │   ├── validators.py              # Validadores customizados
│   │   ├── helpers.py                 # Funções utilitárias
│   │   ├── pagination.py              # Helpers de paginação
│   │   ├── timestamps.py              # Formatação de datas
│   │   └── encryption.py              # Criptografia (senhas, dados sensíveis)
│   │
│   ├── database/                      # Configuração do ORM
│   │   ├── __init__.py
│   │   ├── session.py                 # Database session
│   │   ├── base.py                    # SQLAlchemy declarative base
│   │   └── migrations/                # Alembic migrations
│   │       ├── env.py
│   │       ├── script.py.mako
│   │       ├── alembic.ini
│   │       └── versions/
│   │           ├── 001_initial.py
│   │           ├── 002_add_decisions.py
│   │           └── (... etc)
│   │
│   └── events/                        # Event handlers
│       ├── __init__.py
│       ├── startup.py                 # Evento startup
│       └── shutdown.py                # Evento shutdown
│
├── tests/                             # Testes automatizados
│   ├── __init__.py
│   ├── conftest.py                    # Fixtures pytest
│   ├── test_config.py                 # Config para testes
│   ├── unit/
│   │   ├── test_services/
│   │   ├── test_repositories/
│   │   └── test_utils/
│   ├── integration/
│   │   ├── test_api_auth.py
│   │   ├── test_api_tasks.py
│   │   ├── test_api_decisions.py
│   │   └── test_api_documents.py
│   └── fixtures/
│       ├── users.py
│       ├── projects.py
│       └── tasks.py
│
├── scripts/                           # Scripts de setup/maintenance
│   ├── init_db.py                     # Inicializar BD (tabelas, dados default)
│   ├── seed_demo.py                   # Dados de demo
│   ├── migrate_legacy.py              # Migração de dados legados (CSV/Excel)
│   └── backup.py                      # Backup da BD
│
├── logs/                              # Logs de execução
│   ├── app.log
│   └── audit.log                      # Log separado para auditoria
│
└── docs/                              # Documentação técnica
    ├── API.md                         # Documentação API
    ├── DATABASE.md                    # Schema BD
    ├── PRINCIPLES.md                  # Os 8 princípios implementados
    ├── DEPLOYMENT.md                  # Deploy (Docker, K8s)
    └── CONTRIBUTING.md                # Guia para devs
```

---

## PADRÕES DE CÓDIGO OBRIGATÓRIOS

### 1. **BaseModel (Responsabilidade obrigatória)**
```python
# app/models/base.py
from sqlalchemy import Column, DateTime, String, Integer
from datetime import datetime

class AuditMixin:
    """Mixin que torna responsabilidade rastreável"""
    created_by_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_by_id = Column(Integer, ForeignKey('user.id'))
    updated_at = Column(DateTime, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f"<{self.__class__.__name__} created_by={self.created_by_id} at {self.created_at}>"
```

### 2. **Task Model (Responsável obrigatório)**
```python
# app/models/task.py
from sqlalchemy import Column, String, Integer, Enum
from enum import Enum as PyEnum

class TaskStatus(PyEnum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    BLOCKED = "blocked"

class Task(AuditMixin, Base):
    __tablename__ = "tasks"
    
    id = Column(Integer, primary_key=True)
    project_id = Column(Integer, ForeignKey('projects.id'), nullable=False)
    title = Column(String(255), nullable=False)
    description = Column(Text)
    
    # PRINCÍPIO 1: Responsável obrigatório
    assigned_to_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    assigned_by_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    
    status = Column(Enum(TaskStatus), default=TaskStatus.PENDING)
    due_date = Column(DateTime, nullable=False)
    
    # Sem exceções: todo campo tem rastreabilidade
    __table_args__ = (
        Index('idx_project_responsible', 'project_id', 'assigned_to_id'),
    )
```

### 3. **Decision Model (Princípio 2)**
```python
# app/models/decision.py
class Decision(AuditMixin, Base):
    __tablename__ = "decisions"
    
    id = Column(Integer, primary_key=True)
    project_id = Column(Integer, ForeignKey('projects.id'), nullable=False)
    task_id = Column(Integer, ForeignKey('tasks.id'))
    
    title = Column(String(255), nullable=False)
    content = Column(Text, nullable=False)
    
    # Responsável pela decisão
    decision_maker_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    
    # Assinatura obrigatória
    signed_by_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    signed_at = Column(DateTime, nullable=False)
    signature_hash = Column(String(512))  # Prova de integridade
    
    status = Column(Enum(DecisionStatus), default=DecisionStatus.SIGNED)
```

### 4. **Auditoria Imutável**
```python
# app/models/audit_log.py
class AuditLog(Base):
    __tablename__ = "audit_logs"
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    action = Column(String(50))  # CREATE, UPDATE, DELETE, SIGN
    entity_type = Column(String(50))  # Task, Decision, Document
    entity_id = Column(Integer)
    old_values = Column(JSON)
    new_values = Column(JSON)
    timestamp = Column(DateTime, default=datetime.utcnow, nullable=False, index=True)
    ip_address = Column(String(50))
    user_agent = Column(String(255))
    
    # LOG É IMUTÁVEL - sem UPDATE, sem DELETE
    def __setattr__(self, key, value):
        if key not in ('__dict__', '__mapper__'):
            raise Exception("AuditLog é imutável")
        super().__setattr__(key, value)
```

### 5. **Service Layer Pattern**
```python
# app/services/task_service.py
class TaskService:
    def __init__(self, repo: TaskRepository, audit_service: AuditService):
        self.repo = repo
        self.audit = audit_service
    
    def create_task(self, project_id: int, data: TaskCreate, current_user: User):
        """
        Cria tarefa com responsável obrigatório.
        Sem responsável = ValueError
        """
        if not data.assigned_to_id:
            raise ValueError("Task sem responsável é ilegal em Zentury")
        
        task = Task(
            project_id=project_id,
            **data.dict(),
            created_by_id=current_user.id
        )
        self.repo.save(task)
        
        # Registar na auditoria
        self.audit.log(
            user_id=current_user.id,
            action="CREATE",
            entity_type="Task",
            entity_id=task.id,
            new_values=task.to_dict()
        )
        return task
```

### 6. **Middleware de Rastreabilidade**
```python
# app/core/middleware.py
from starlette.middleware.base import BaseHTTPMiddleware

class AuditMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        # Capturar user, IP, user-agent antes da requisição
        user_id = request.state.user_id if hasattr(request.state, 'user_id') else None
        ip = request.client.host
        
        response = await call_next(request)
        
        # Registar se foi mutação (POST, PUT, DELETE)
        if request.method in ["POST", "PUT", "DELETE"]:
            await self.log_mutation(user_id, request.method, request.url.path, ip)
        
        return response
```

---

## REGRAS NÃO-NEGOÇÁVEIS

✅ **Cada INSERT/UPDATE/DELETE tem user_id e timestamp**
✅ **Nenhuma ação anónima no sistema**
✅ **Decisions são signed_at + signature_hash (prova)**
✅ **AuditLog é append-only (sem UPDATE)**
✅ **Task sem assigned_to_id = validação falha**
✅ **Document sem version = travado**
✅ **Sem "draft" infinito - ciclo de vida claro**

---

## PRÓXIMAS COISAS CRÍTICAS

1. **Database schema (.sql ou Alembic migrations)**
2. **FastAPI routes (endpoints concretos)**
3. **Pydantic schemas (validação rigorosa)**
4. **Tests (pytest - nada sem testes)**

Quer que eu crie agora?

Qual prioridade:
1️⃣ **Database schema SQL completo**
2️⃣ **Modelos SQLAlchemy + Pydantic schemas**
3️⃣ **FastAPI routes skeleton**
4️⃣ **Docker + docker-compose setup**