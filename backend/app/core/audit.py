"""
ZENTURY - Audit Service
Sistema de auditoria imutável - Princípio 5
"""

import json
from datetime import datetime
from typing import Optional, Any, Dict
from enum import Enum
import logging

logger = logging.getLogger(__name__)

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

class AuditService:
    """Serviço de auditoria - Princípio 5"""
    
    @staticmethod
    def log_action(
        db_session,
        user_id: int,
        action: AuditAction,
        entity_type: str,
        entity_id: int,
        old_values: Optional[Dict[str, Any]] = None,
        new_values: Optional[Dict[str, Any]] = None,
        ip_address: Optional[str] = None,
        user_agent: Optional[str] = None,
    ) -> None:
        """Registar uma ação no log de auditoria"""
        from app.models.base import AuditLog
        
        try:
            audit_entry = AuditLog(
                user_id=user_id,
                action=action.value,
                entity_type=entity_type,
                entity_id=entity_id,
                old_values=old_values,
                new_values=new_values,
                timestamp=datetime.utcnow(),
                ip_address=ip_address,
                user_agent=user_agent,
            )
            
            db_session.add(audit_entry)
            db_session.commit()
            
            logger.info(
                f"✅ AUDITORIA: {action.value} {entity_type}:{entity_id} "
                f"por usuário {user_id}"
            )
            
        except Exception as e:
            logger.error(f"❌ ERRO ao registar auditoria: {str(e)}")
            db_session.rollback()
            raise
    
    @staticmethod
    def log_create(
        db_session,
        user_id: int,
        entity_type: str,
        entity_id: int,
        new_values: Dict[str, Any],
        ip_address: Optional[str] = None,
        user_agent: Optional[str] = None,
    ) -> None:
        """Registar criação"""
        AuditService.log_action(
            db_session=db_session,
            user_id=user_id,
            action=AuditAction.CREATE,
            entity_type=entity_type,
            entity_id=entity_id,
            new_values=new_values,
            ip_address=ip_address,
            user_agent=user_agent,
        )
    
    @staticmethod
    def log_update(
        db_session,
        user_id: int,
        entity_type: str,
        entity_id: int,
        old_values: Dict[str, Any],
        new_values: Dict[str, Any],
        ip_address: Optional[str] = None,
        user_agent: Optional[str] = None,
    ) -> None:
        """Registar atualização"""
        AuditService.log_action(
            db_session=db_session,
            user_id=user_id,
            action=AuditAction.UPDATE,
            entity_type=entity_type,
            entity_id=entity_id,
            old_values=old_values,
            new_values=new_values,
            ip_address=ip_address,
            user_agent=user_agent,
        )
    
    @staticmethod
    def log_sign(
        db_session,
        user_id: int,
        entity_type: str,
        entity_id: int,
        ip_address: Optional[str] = None,
        user_agent: Optional[str] = None,
    ) -> None:
        """Registar assinatura"""
        AuditService.log_action(
            db_session=db_session,
            user_id=user_id,
            action=AuditAction.SIGN,
            entity_type=entity_type,
            entity_id=entity_id,
            ip_address=ip_address,
            user_agent=user_agent,
        )
    
    @staticmethod
    def log_approve(
        db_session,
        user_id: int,
        entity_type: str,
        entity_id: int,
        ip_address: Optional[str] = None,
        user_agent: Optional[str] = None,
    ) -> None:
        """Registar aprovação"""
        AuditService.log_action(
            db_session=db_session,
            user_id=user_id,
            action=AuditAction.APPROVE,
            entity_type=entity_type,
            entity_id=entity_id,
            ip_address=ip_address,
            user_agent=user_agent,
        )
    
    @staticmethod
    def get_entity_history(db_session, entity_type: str, entity_id: int):
        """Obter histórico completo"""
        from app.models.base import AuditLog
        
        logs = db_session.query(AuditLog).filter(
            AuditLog.entity_type == entity_type,
            AuditLog.entity_id == entity_id,
        ).order_by(AuditLog.timestamp.desc()).all()
        
        return logs