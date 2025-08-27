from fastapi import Depends, HTTPException, status, UploadFile
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from typing import Optional, Dict, Any
import logging

from app.core.token_generator import verify_token as verify_jwt_token
from app.services.application_facade import ApplicationFacade
from app.services.implementations.admin_service import JwtAdminService
from app.services.implementations.document_service import PdfDocumentService
from app.services.implementations.document_service import QdrantVectorService
from app.services.implementations.pdf_processor import PdfProcessor
from app.services.implementations.local_llm_service import LocalLlmService


# Repositories
from app.persistence.mongodb.admin_repository import AdminMongoRepository
from app.persistence.mongodb.document_repository import DocumentMongoRepository
from app.persistence.qdrant.vector_repository import VectorQdrantRepository

from app.api.schemas.auth import TokenData
logger = logging.getLogger(__name__)
security = HTTPBearer()

# ==================== SERVICE FACTORY ====================

class ServiceFactory:
    """Factory pour créer et injecter les services"""
    
    def __init__(self):
        # Repositories
        self._admin_repo = AdminMongoRepository()
        self._document_repo = DocumentMongoRepository()
        self._vector_repo = VectorQdrantRepository()
        
        # Services
        self._admin_service = None
        self._document_service = None
        self._vector_service = None
        self._llm_service = None
        self._pdf_processor = None
        self._facade = None
    
    def get_admin_service(self) -> JwtAdminService:
        if self._admin_service is None:
            self._admin_service = JwtAdminService(self._admin_repo)
        return self._admin_service
    
    def get_vector_service(self) -> QdrantVectorService:
        if self._vector_service is None:
            self._vector_service = QdrantVectorService(self._vector_repo)
        return self._vector_service
    
    def get_llm_service(self) -> LocalLlmService:
        if self._llm_service is None:
            self._llm_service = LocalLlmService()
        return self._llm_service
    
    def get_pdf_processor(self) -> PdfProcessor:
        if self._pdf_processor is None:
            self._pdf_processor = PdfProcessor()
        return self._pdf_processor
    
    def get_document_service(self) -> PdfDocumentService:
        if self._document_service is None:
            self._document_service = PdfDocumentService(
                self._document_repo,
                self.get_vector_service(),
                self.get_pdf_processor()
            )
        return self._document_service
    
    def get_application_facade(self) -> ApplicationFacade:
        if self._facade is None:
            self._facade = ApplicationFacade(
                self.get_admin_service(),
                self.get_document_service(),
                self.get_vector_service(),
                self.get_llm_service()
            )
        return self._facade

# Instance globale du factory
service_factory = ServiceFactory()

# ==================== DEPENDENCIES ====================

def get_services() -> ApplicationFacade:
    """Dépendance pour obtenir la facade des services"""
    return service_factory.get_application_facade()

def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)) -> Dict[str, Any]:
    """
    Dépendance pour vérifier le token et récupérer l'utilisateur actuel
    """
    try:
        token = credentials.credentials
        payload = verify_jwt_token(token)
        return payload
    except Exception as e:
        logger.error(f"Erreur de validation du token: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token invalide",
            headers={"WWW-Authenticate": "Bearer"},
        )

def require_admin(current_user: TokenData = Depends(get_current_user)) -> TokenData:
    """
    Dépendance pour s'assurer que l'utilisateur est un admin
    """
    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Accès refusé - Droits administrateur requis"
        )
    return current_user


def optional_auth(
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(HTTPBearer(auto_error=False))
) -> Optional[Dict[str, Any]]:
    """
    Dépendance pour une authentification optionnelle.
    Retourne les infos du token si elles existent, sinon None.
    """
    if not credentials:
        return None

    try:
        token = credentials.credentials
        return verify_jwt_token(token)
    except Exception:
        return None

def validate_file_upload(file: UploadFile) -> UploadFile:
    """
    Valide le fichier uploadé
    """
    # Vérifier le type MIME
    if not file.content_type or not file.content_type.startswith("application/pdf"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Seuls les fichiers PDF sont acceptés"
        )
    
    # Vérifier la taille (exemple: max 50MB)
    max_size = 50 * 1024 * 1024  # 50MB
    if hasattr(file, 'size') and file.size and file.size > max_size:
        raise HTTPException(
            status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            detail="Fichier trop volumineux (max 50MB)"
        )
    
    return file

def paginate(skip: int = 0, limit: int = 100) -> Dict[str, int]:
    """
    Dépendance pour la pagination
    """
    if skip < 0:
        skip = 0
    if limit <= 0 or limit > 1000:
        limit = 100
    
    return {"skip": skip, "limit": limit}