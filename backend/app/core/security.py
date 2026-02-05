"""
ZENTURY - Security Module
JWT, OAuth2, hashing, assinatura digital
"""

from datetime import datetime, timedelta
from typing import Optional, Dict, Any
from passlib.context import CryptContext
from jose import JWTError, jwt
import logging
import hashlib

logger = logging.getLogger(__name__)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class SecurityService:
    """Serviço de segurança"""
    
    @staticmethod
    def hash_password(password: str) -> str:
        return pwd_context.hash(password)
    
    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        return pwd_context.verify(plain_password, hashed_password)
    
    @staticmethod
    def create_access_token(
        data: Dict[str, Any],
        secret_key: str,
        algorithm: str = "HS256",
        expires_delta: Optional[timedelta] = None,
    ) -> str:
        to_encode = data.copy()
        
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=30)
        
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, secret_key, algorithm=algorithm)
        
        logger.info(f"✅ Access token criado para user: {data.get('sub')}")
        return encoded_jwt
    
    @staticmethod
    def create_refresh_token(
        data: Dict[str, Any],
        secret_key: str,
        algorithm: str = "HS256",
        expires_delta: Optional[timedelta] = None,
    ) -> str:
        to_encode = data.copy()
        
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(days=7)
        
        to_encode.update({"exp": expire, "type": "refresh"})
        encoded_jwt = jwt.encode(to_encode, secret_key, algorithm=algorithm)
        
        logger.info(f"✅ Refresh token criado para user: {data.get('sub')}")
        return encoded_jwt
    
    @staticmethod
    def decode_token(
        token: str,
        secret_key: str,
        algorithm: str = "HS256",
    ) -> Optional[Dict[str, Any]]:
        try:
            payload = jwt.decode(token, secret_key, algorithms=[algorithm])
            return payload
        except JWTError as e:
            logger.warning(f"❌ Token inválido: {str(e)}")
            return None

class PermissionService:
    """Serviço de permissões"""
    
    @staticmethod
    def has_permission(user_role: str, required_permission: str) -> bool:
        from app.core.constants import PERMISSION_MATRIX
        
        if user_role not in PERMISSION_MATRIX:
            logger.warning(f"❌ Role desconhecido: {user_role}")
            return False
        
        permissions = PERMISSION_MATRIX[user_role]
        has_perm = required_permission in permissions
        
        if not has_perm:
            logger.warning(
                f"❌ Permissão negada: {user_role} tentou {required_permission}"
            )
        
        return has_perm
    
    @staticmethod
    def require_permission(user_role: str, required_permission: str) -> None:
        from app.core.exceptions import InsufficientPermissionsException
        
        if not PermissionService.has_permission(user_role, required_permission):
            raise InsufficientPermissionsException(required_permission)
    
    @staticmethod
    def get_user_permissions(user_role: str) -> list:
        from app.core.constants import PERMISSION_MATRIX
        
        if user_role not in PERMISSION_MATRIX:
            return []
        
        return PERMISSION_MATRIX[user_role]

class SignatureService:
    """Serviço de assinatura digital"""
    
    @staticmethod
    def generate_signature_hash(
        data: str,
        user_id: int,
        timestamp: datetime,
    ) -> str:
        combined = f"{data}:{user_id}:{timestamp.isoformat()}"
        signature_hash = hashlib.sha256(combined.encode()).hexdigest()
        
        logger.info(f"✅ Assinatura gerada: {signature_hash[:16]}...")
        return signature_hash
    
    @staticmethod
    def verify_signature(
        data: str,
        user_id: int,
        timestamp: datetime,
        expected_hash: str,
    ) -> bool:
        computed_hash = SignatureService.generate_signature_hash(
            data, user_id, timestamp
        )
        
        is_valid = computed_hash == expected_hash
        
        if is_valid:
            logger.info(f"✅ Assinatura válida: {expected_hash[:16]}...")
        else:
            logger.warning(f"❌ Assinatura INVÁLIDA: {expected_hash[:16]}...")
        
        return is_valid