# app/api/routes/document.py
from fastapi import APIRouter, UploadFile, File, Form, HTTPException, status, Depends
from typing import List
import logging
import time

from app.api.schemas.document import (
    UploadResponse, DocumentListResponse, DeleteResponse, 
    DocumentMetadata, DocumentDetailResponse
)
from app.api.deps import get_services, require_admin, validate_file_upload, paginate
from app.services.application_facade import ApplicationFacade

router = APIRouter(prefix="/documents", tags=["Documents"])
logger = logging.getLogger(__name__)

@router.post("/upload",
             response_model=UploadResponse,
             summary="Uploader un fichier PDF",
             description="Upload et vectorise un fichier PDF")
async def upload_pdf(
    system_name: str = Form(..., description="Nom du système source"),
    file: UploadFile = File(..., description="Fichier PDF à uploader"),
    current_user: dict = Depends(require_admin),
    services: ApplicationFacade = Depends(get_services),
    validated_file: UploadFile = Depends(validate_file_upload)
):
    """
    Upload, traite et vectorise un fichier PDF
    """
    start_time = time.time()
    
    try:
        logger.info(f"Upload du fichier '{file.filename}'")
        
        # Reset file pointer after validation
        await file.seek(0)
        
        result = await services.upload_and_vectorize_document(file, system_name)
        
        processing_time = time.time() - start_time
        logger.info(f"Fichier '{file.filename}' traité en {processing_time:.2f}s")
        
        return UploadResponse(
            status=result["status"],
            message=result["message"],
            file_hash=result["file_hash"],
            document_id=result.get("document_id")
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Erreur lors de l'upload: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erreur lors du traitement du fichier"
        )

@router.get("/",
            response_model=DocumentListResponse,
            summary="Lister tous les documents",
            description="Récupère la liste de tous les documents vectorisés")
async def list_documents(
    current_user: dict = Depends(require_admin),
    services: ApplicationFacade = Depends(get_services),
    pagination: dict = Depends(paginate)
):
    """
    Récupère la liste paginée des documents
    """
    try:
        documents_data = services.get_all_documents()
        
        # Application de la pagination
        skip = pagination["skip"]
        limit = pagination["limit"]
        
        total = len(documents_data)
        paginated_docs = documents_data[skip:skip + limit]
        
        # Conversion en schéma Pydantic
        documents = [
            DocumentMetadata(**doc) for doc in paginated_docs
        ]
        
        return DocumentListResponse(
            documents=documents,
            total=total
        )
        
    except Exception as e:
        logger.error(f"Erreur lors de la récupération des documents: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erreur lors de la récupération des documents"
        )

@router.get("/{file_hash}",
            response_model=DocumentDetailResponse,
            summary="Détails d'un document",
            description="Récupère les détails d'un document par son hash")
async def get_document_details(
    file_hash: str,
    current_user: dict = Depends(require_admin),
    services: ApplicationFacade = Depends(get_services)
):
    """
    Récupère les détails d'un document spécifique
    """
    try:
        doc_data = services.get_document_by_hash(file_hash)
        
        if "error" in doc_data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Document non trouvé"
            )
        
        metadata = DocumentMetadata(**doc_data)
        
        return DocumentDetailResponse(
            metadata=metadata,
            chunks_count=doc_data.get("chunks_count"),
            last_accessed=doc_data.get("last_accessed")
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Erreur lors de la récupération du document: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erreur lors de la récupération du document"
        )

@router.delete("/{file_hash}",
               response_model=DeleteResponse,
               summary="Supprimer un document",
               description="Supprime un document par son hash")
async def delete_document(
    file_hash: str,
    current_user: dict = Depends(require_admin),
    services: ApplicationFacade = Depends(get_services)
):
    """
    Supprime un document et tous ses chunks associés
    """
    try:
        logger.info(f"Suppression du document {file_hash}")
        
        result = services.delete_document_by_hash(file_hash)
        
        return DeleteResponse(
            status=result.get("status", "success"),
            message=result.get("message", "Document supprimé"),
            file_hash=file_hash
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Erreur lors de la suppression: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erreur lors de la suppression du document"
        )

@router.get("/health/check",
            summary="Vérification de santé",
            description="Vérifie le statut des services de documents")
async def health_check(
    services: ApplicationFacade = Depends(get_services)
):
    """
    Endpoint de vérification de santé
    """
    try:
        health_status = services.health_check()
        return health_status
        
    except Exception as e:
        logger.error(f"Erreur lors du health check: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Services indisponibles"
        )
