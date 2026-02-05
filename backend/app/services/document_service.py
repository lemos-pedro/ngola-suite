"""
ZENTURY - Document Service
Implementa Princípio 3: Documento é Ativo Operacional
Documento tem ciclo de vida: draft → in_review → approved → signed
"""

import logging
from typing import Optional
from datetime import datetime

logger = logging.getLogger(__name__)

class DocumentService:
    """
    Serviço de documentos.
    Respeitando Princípio 3: Documento é Ativo Operacional com ciclo de vida.
    """
    
    @staticmethod
    def create_document(
        db_session,
        project_id: int,
        title: str,
        content: str,
        current_user_id: int,
    ):
        """
        Criar documento em estado DRAFT.
        
        Princípio 3: Documento tem ciclo de vida claro.
        Começa em DRAFT, não pode prosseguir sem aprovação.
        """
        from app.models.base import Document
        from app.core.audit import AuditService
        
        logger.info(
            f"✅ Criando Document: '{title}' "
            f"em status DRAFT"
        )
        
        # Criar entidade em DRAFT
        document = Document(
            project_id=project_id,
            title=title,
            content=content,
            version=1,
            status="draft",  # Começa em draft
            created_by_id=current_user_id,
        )
        
        # Salvar no banco
        db_session.add(document)
        db_session.flush()  # Para obter ID
        
        # Registar auditoria
        AuditService.log_create(
            db_session=db_session,
            user_id=current_user_id,
            entity_type="Document",
            entity_id=document.id,
            new_values={
                "title": title,
                "status": "draft",
                "version": 1,
            },
        )
        
        db_session.commit()
        
        return document
    
    @staticmethod
    def submit_for_review(
        db_session,
        document_id: int,
        current_user_id: int,
    ):
        """
        Submeter documento para revisão.
        draft → in_review
        """
        from app.models.base import Document
        from app.core.exceptions import DocumentNotFoundException, StateConflictException
        from app.core.audit import AuditService
        
        document = db_session.query(Document).filter(Document.id == document_id).first()
        if not document:
            raise DocumentNotFoundException(document_id)
        
        # Validar transição de estado
        if document.status != "draft":
            raise StateConflictException(document.status, "in_review")
        
        # Atualizar status
        document.status = "in_review"
        document.updated_by_id = current_user_id
        document.updated_at = datetime.utcnow()
        
        # Registar auditoria
        AuditService.log_update(
            db_session=db_session,
            user_id=current_user_id,
            entity_type="Document",
            entity_id=document_id,
            old_values={"status": "draft"},
            new_values={"status": "in_review"},
        )
        
        db_session.commit()
        
        logger.info(f"✅ Document {document_id} submetido para revisão")
        
        return document
    
    @staticmethod
    def approve_document(
        db_session,
        document_id: int,
        approver_id: int,
        current_user_id: int,
    ):
        """
        Aprovar documento.
        in_review → approved
        
        Princípio 3: Documento precisa de aprovação.
        """
        from app.models.base import Document
        from app.core.exceptions import DocumentNotFoundException, StateConflictException
        from app.core.audit import AuditService
        
        document = db_session.query(Document).filter(Document.id == document_id).first()
        if not document:
            raise DocumentNotFoundException(document_id)
        
        # Validar transição de estado
        if document.status != "in_review":
            raise StateConflictException(document.status, "approved")
        
        # Atualizar status
        document.status = "approved"
        document.approved_by_id = approver_id
        document.approved_at = datetime.utcnow()
        document.updated_by_id = current_user_id
        document.updated_at = datetime.utcnow()
        
        # Registar auditoria
        AuditService.log_approve(
            db_session=db_session,
            user_id=current_user_id,
            entity_type="Document",
            entity_id=document_id,
        )
        
        db_session.commit()
        
        logger.info(f"✅ Document {document_id} aprovado por {approver_id}")
        
        return document
    
    @staticmethod
    def sign_document(
        db_session,
        document_id: int,
        signer_id: int,
        current_user_id: int,
    ):
        """
        Assinar documento.
        approved → signed
        
        Princípio 3: Documento precisa de assinatura para ser válido.
        """
        from app.models.base import Document
        from app.core.exceptions import DocumentNotFoundException, StateConflictException
        from app.core.security import SignatureService
        from app.core.audit import AuditService
        
        document = db_session.query(Document).filter(Document.id == document_id).first()
        if not document:
            raise DocumentNotFoundException(document_id)
        
        # Validar transição de estado
        if document.status != "approved":
            raise StateConflictException(document.status, "signed")
        
        # Gerar assinatura
        signature_hash = SignatureService.generate_signature_hash(
            data=document.content,
            user_id=signer_id,
            timestamp=datetime.utcnow(),
        )
        
        # Atualizar status
        document.status = "signed"
        document.signed_by_id = signer_id
        document.signed_at = datetime.utcnow()
        document.signature_hash = signature_hash
        document.updated_by_id = current_user_id
        document.updated_at = datetime.utcnow()
        
        # Registar auditoria
        AuditService.log_sign(
            db_session=db_session,
            user_id=current_user_id,
            entity_type="Document",
            entity_id=document_id,
        )
        
        db_session.commit()
        
        logger.info(f"✅ Document {document_id} assinado por {signer_id}")
        
        return document
    
    @staticmethod
    def get_document(db_session, document_id: int):
        """Obter documento por ID"""
        from app.models.base import Document
        from app.core.exceptions import DocumentNotFoundException
        
        document = db_session.query(Document).filter(Document.id == document_id).first()
        if not document:
            raise DocumentNotFoundException(document_id)
        
        return document
    
    @staticmethod
    def list_documents(
        db_session,
        project_id: Optional[int] = None,
        status: Optional[str] = None,
        limit: int = 50,
        offset: int = 0,
    ):
        """Listar documentos com filtros"""
        from app.models.base import Document
        
        query = db_session.query(Document)
        
        if project_id:
            query = query.filter(Document.project_id == project_id)
        
        if status:
            query = query.filter(Document.status == status)
        
        total = query.count()
        documents = query.offset(offset).limit(limit).all()
        
        return {"total": total, "documents": documents}