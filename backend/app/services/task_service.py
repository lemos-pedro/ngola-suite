"""
ZENTURY - Task Service
Implementa Princípio 1: Responsabilidade é o Centro
Todo Task DEVE ter assigned_to_id. Sem isso, exceção.
"""

import logging
from typing import Optional, List
from datetime import datetime

logger = logging.getLogger(__name__)

class TaskService:
    """
    Serviço de tarefas.
    Respeitando Princípio 1: NADA é anónimo.
    """
    
    @staticmethod
    def create_task(
        db_session,
        project_id: int,
        title: str,
        description: str,
        assigned_to_id: int,  # ← OBRIGATÓRIO
        assigned_by_id: int,  # Quem atribuiu
        due_date: datetime,
        current_user_id: int,
    ):
        """
        Criar tarefa.
        
        REGRA ABSOLUTA (Princípio 1):
        - assigned_to_id é NOT NULL (não pode ser None)
        - Se não houver responsável, lança TaskMissingAssigneeException
        """
        from app.models.base import Task
        from app.core.exceptions import TaskMissingAssigneeException
        from app.core.audit import AuditService
        
        # VALIDAÇÃO (Princípio 1)
        if not assigned_to_id:
            raise TaskMissingAssigneeException()
        
        logger.info(
            f"✅ Criando Task: '{title}' "
            f"assigned_to={assigned_to_id} "
            f"by={assigned_by_id}"
        )
        
        # Criar entidade
        task = Task(
            project_id=project_id,
            title=title,
            description=description,
            assigned_to_id=assigned_to_id,
            assigned_by_id=assigned_by_id,
            due_date=due_date,
            created_by_id=current_user_id,
            status="pending",
        )
        
        # Salvar no banco
        db_session.add(task)
        db_session.flush()  # Para obter ID
        
        # Registar auditoria (Princípio 5)
        AuditService.log_create(
            db_session=db_session,
            user_id=current_user_id,
            entity_type="Task",
            entity_id=task.id,
            new_values={
                "title": title,
                "assigned_to_id": assigned_to_id,
                "assigned_by_id": assigned_by_id,
                "due_date": due_date.isoformat(),
            },
        )
        
        db_session.commit()
        
        return task
    
    @staticmethod
    def update_task(
        db_session,
        task_id: int,
        title: Optional[str] = None,
        description: Optional[str] = None,
        assigned_to_id: Optional[int] = None,
        status: Optional[str] = None,
        due_date: Optional[datetime] = None,
        current_user_id: int = None,
    ):
        """
        Atualizar tarefa.
        
        Princípio 1: assigned_to_id não pode virar None.
        """
        from app.models.base import Task
        from app.core.exceptions import TaskMissingAssigneeException, TaskNotFoundException
        from app.core.audit import AuditService
        
        # Obter tarefa existente
        task = db_session.query(Task).filter(Task.id == task_id).first()
        if not task:
            raise TaskNotFoundException(task_id)
        
        # Guardar valores antigos para auditoria
        old_values = {
            "title": task.title,
            "assigned_to_id": task.assigned_to_id,
            "status": task.status,
        }
        
        # Atualizar campos
        if title:
            task.title = title
        if description:
            task.description = description
        if assigned_to_id:
            task.assigned_to_id = assigned_to_id
        elif assigned_to_id is None and "assigned_to_id" in locals():
            # Se tentou passar None explicitamente, rejeita
            raise TaskMissingAssigneeException()
        
        if status:
            task.status = status
        if due_date:
            task.due_date = due_date
        
        task.updated_by_id = current_user_id
        task.updated_at = datetime.utcnow()
        
        # Registar auditoria
        new_values = {
            "title": task.title,
            "assigned_to_id": task.assigned_to_id,
            "status": task.status,
        }
        
        AuditService.log_update(
            db_session=db_session,
            user_id=current_user_id,
            entity_type="Task",
            entity_id=task_id,
            old_values=old_values,
            new_values=new_values,
        )
        
        db_session.commit()
        
        logger.info(f"✅ Task atualizada: {task_id}")
        
        return task
    
    @staticmethod
    def get_task(db_session, task_id: int):
        """Obter tarefa por ID"""
        from app.models.base import Task
        from app.core.exceptions import TaskNotFoundException
        
        task = db_session.query(Task).filter(Task.id == task_id).first()
        if not task:
            raise TaskNotFoundException(task_id)
        
        return task
    
    @staticmethod
    def list_tasks(
        db_session,
        project_id: Optional[int] = None,
        assigned_to_id: Optional[int] = None,
        status: Optional[str] = None,
        limit: int = 50,
        offset: int = 0,
    ):
        """Listar tarefas com filtros"""
        from app.models.base import Task
        
        query = db_session.query(Task)
        
        if project_id:
            query = query.filter(Task.project_id == project_id)
        
        if assigned_to_id:
            query = query.filter(Task.assigned_to_id == assigned_to_id)
        
        if status:
            query = query.filter(Task.status == status)
        
        total = query.count()
        tasks = query.offset(offset).limit(limit).all()
        
        return {"total": total, "tasks": tasks}
    
    @staticmethod
    def change_task_status(
        db_session,
        task_id: int,
        new_status: str,
        current_user_id: int,
    ):
        """Mudar status de uma tarefa"""
        from app.models.base import Task
        from app.core.exceptions import TaskNotFoundException
        from app.core.audit import AuditService
        
        task = db_session.query(Task).filter(Task.id == task_id).first()
        if not task:
            raise TaskNotFoundException(task_id)
        
        old_status = task.status
        task.status = new_status
        task.updated_by_id = current_user_id
        task.updated_at = datetime.utcnow()
        
        # Registar auditoria
        AuditService.log_update(
            db_session=db_session,
            user_id=current_user_id,
            entity_type="Task",
            entity_id=task_id,
            old_values={"status": old_status},
            new_values={"status": new_status},
        )
        
        db_session.commit()
        
        logger.info(f"✅ Task status atualizado: {task_id} → {new_status}")
        
        return task