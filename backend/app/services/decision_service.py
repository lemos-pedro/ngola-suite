"""
ZENTURY - Decision Service
Implementa Princípio 2: Decisão não é Chat
Decisão é objeto próprio com assinatura e timestamp.
"""

import logging
from typing import Optional
from datetime import datetime

logger = logging.getLogger(__name__)

class DecisionService:
    """
    Serviço de decisões.
    Respeitando Princípio 2: Decisão é objeto próprio, assinado.
    """
    
    @staticmethod
    def create_decision(
        db_session,
        project_id: int,
        task_id: Optional[int],
        title: str,
        content: str,
        decision_maker_id: int,  # Quem toma a decisão
        signed_by_id: int,  # Quem assina (pode ser o mesmo)
        current_user_id: int,
    ):
        """
        Criar decisão.
        
        REGRA ABSOLUTA (Princípio 2):
        - Decisão DEVE ter assinatura
        - signature_hash é obrigatório
        - signed_at é NOT NULL
        """
        from app.models.base import Decision
        from app.core.exceptions import DecisionNotSignedException
        from app.core.security import SignatureService
        from app.core.audit import AuditService
        
        logger.info(
            f"✅ Criando Decision: '{title}' "
            f"maker={decision_maker_id} "
            f"signed_by={signed_by_id}"
        )
        
        # Gerar assinatura (Princípio 2)
        signature_hash = SignatureService.generate_signature_hash(
            data=content,
            user_id=signed_by_id,
            timestamp=datetime.utcnow(),
        )
        
        # Criar entidade
        decision = Decision(
            project_id=project_id,
            task_id=task_id,
            title=title,
            content=content,
            decision_maker_id=decision_maker_id,
            signed_by_id=signed_by_id,
            signed_at=datetime.utcnow(),
            signature_hash=signature_hash,
            status="signed",
            created_by_id=current_user_id,
        )
        
        # Salvar no banco
        db_session.add(decision)
        db_session.flush()  # Para obter ID
        
        # Registar auditoria (Princípio 5)
        AuditService.log_sign(
            db_session=db_session,
            user_id=current_user_id,
            entity_type="Decision",
            entity_id=decision.id,
        )
        
        db_session.commit()
        
        return decision
    
    @staticmethod
    def get_decision(db_session, decision_id: int):
        """Obter decisão por ID"""
        from app.models.base import Decision
        from app.core.exceptions import DecisionNotFoundException
        
        decision = db_session.query(Decision).filter(Decision.id == decision_id).first()
        if not decision:
            raise DecisionNotFoundException(decision_id)
        
        return decision
    
    @staticmethod
    def list_decisions(
        db_session,
        project_id: Optional[int] = None,
        task_id: Optional[int] = None,
        status: Optional[str] = None,
        limit: int = 50,
        offset: int = 0,
    ):
        """Listar decisões com filtros"""
        from app.models.base import Decision
        
        query = db_session.query(Decision)
        
        if project_id:
            query = query.filter(Decision.project_id == project_id)
        
        if task_id:
            query = query.filter(Decision.task_id == task_id)
        
        if status:
            query = query.filter(Decision.status == status)
        
        total = query.count()
        decisions = query.offset(offset).limit(limit).all()
        
        return {"total": total, "decisions": decisions}
    
    @staticmethod
    def verify_decision_signature(db_session, decision_id: int) -> bool:
        """
        Verificar se assinatura de decisão é válida.
        Princípio 2: Decisão deve ser assinada.
        """
        from app.core.security import SignatureService
        
        decision = DecisionService.get_decision(db_session, decision_id)
        
        # Recompor assinatura
        is_valid = SignatureService.verify_signature(
            data=decision.content,
            user_id=decision.signed_by_id,
            timestamp=decision.signed_at,
            expected_hash=decision.signature_hash,
        )
        
        if is_valid:
            logger.info(f"✅ Decisão {decision_id} assinatura válida")
        else:
            logger.error(f"❌ Decisão {decision_id} assinatura INVÁLIDA")
        
        return is_valid
    
    @staticmethod
    def supersede_decision(
        db_session,
        old_decision_id: int,
        new_decision_id: int,
        current_user_id: int,
    ):
        """
        Marcar decisão antiga como supersedida por nova.
        Respeitando Princípio 2: Histórico de decisões.
        """
        from app.models.base import Decision
        from app.core.exceptions import DecisionNotFoundException
        from app.core.audit import AuditService
        
        old_decision = db_session.query(Decision).filter(
            Decision.id == old_decision_id
        ).first()
        if not old_decision:
            raise DecisionNotFoundException(old_decision_id)
        
        new_decision = db_session.query(Decision).filter(
            Decision.id == new_decision_id
        ).first()
        if not new_decision:
            raise DecisionNotFoundException(new_decision_id)
        
        # Marcar como supersedida
        old_decision.status = "superseded"
        old_decision.updated_by_id = current_user_id
        old_decision.updated_at = datetime.utcnow()
        
        # Registar auditoria
        AuditService.log_update(
            db_session=db_session,
            user_id=current_user_id,
            entity_type="Decision",
            entity_id=old_decision_id,
            old_values={"status": "signed"},
            new_values={"status": "superseded"},
        )
        
        db_session.commit()
        
        logger.info(
            f"✅ Decisão {old_decision_id} marcada como "
            f"supersedida por {new_decision_id}"
        )
        
        return old_decision