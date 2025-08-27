# app/services/implementations/document_service.py
from fastapi import HTTPException, UploadFile
from typing import List, Dict, Optional
import logging

from app.services.interfaces.document_interface import DocumentInterface
from app.services.implementations.pdf_processor import PdfProcessor
from app.services.implementations.vector_service import QdrantVectorService
from app.persistence.interfaces.document_repository import AbstractDocumentRepository
from app.models.pdf_metadata import PDFMetadata

logger = logging.getLogger(__name__)

class PdfDocumentService(DocumentInterface):
    def __init__(self, 
                 document_repository: AbstractDocumentRepository,
                 vector_service: QdrantVectorService,
                 pdf_processor: PdfProcessor):
        self.document_repository = document_repository
        self.vector_service = vector_service
        self.pdf_processor = pdf_processor
    
    async def upload_and_process(self, file: UploadFile, system_name: str) -> Dict:
        try:
            # Sauvegarde et extraction du texte
            file_path = self.pdf_processor.save_uploaded_pdf(file)
            full_text = self.pdf_processor.extract_full_text(file_path)
            cleaned_text = self.pdf_processor.clean_text(full_text)
            
            # Vectorisation
            qdrant_dtos, pdf_metadata = await self.pdf_processor.vectorize_text(
                text=cleaned_text,
                file_name=file.filename,
                system_name=system_name,
            )
            
            content_hash = pdf_metadata.file_hash
            
            # Vérification doublon
            if self.document_repository.find_by_hash(content_hash) is None:
                # Ajout dans le store vectoriel
                self.vector_service.add_documents(qdrant_dtos)
                
                # Sauvegarde des métadonnées
                doc_id = self.document_repository.insert_pdf_metadata(pdf_metadata)
                
                return {
                    "status": "success",
                    "message": "Document vectorisé avec succès",
                    "file_hash": content_hash,
                    "document_id": doc_id
                }
            else:
                raise HTTPException(
                    status_code=400, 
                    detail="Le fichier a déjà été vectorisé !"
                )
                
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Erreur lors du traitement du document: {str(e)}")
            raise HTTPException(
                status_code=500,
                detail="Erreur lors du traitement du document"
            )
    
    def get_all_documents(self) -> List[Dict]:
        try:
            documents: List[PDFMetadata] = self.document_repository.list_documents()
            cleaned_docs = []
            
            for doc in documents:
                doc_dict = doc.__dict__.copy() if hasattr(doc, "__dict__") else dict(doc)
                doc_dict.pop("_id", None)  # Nettoyage ID Mongo
                cleaned_docs.append(doc_dict)
            
            return cleaned_docs
            
        except Exception as e:
            logger.error(f"Erreur lors de la récupération des documents: {str(e)}")
            raise HTTPException(
                status_code=500,
                detail="Erreur lors de la récupération des documents"
            )
    
    def delete_document(self, file_hash: str) -> Dict:
        try:
            # Suppression du store vectoriel
            deleted_vector = self.vector_service.delete_document(file_hash)
            
            if deleted_vector:
                # Suppression des métadonnées
                deleted_metadata = self.document_repository.delete_by_hash(file_hash)
                
                if deleted_metadata:
                    return {
                        "status": "success",
                        "message": "Document supprimé avec succès"
                    }
                else:
                    raise HTTPException(
                        status_code=500, 
                        detail="Erreur lors de la suppression dans MongoDB"
                    )
            else:
                raise HTTPException(
                    status_code=404, 
                    detail="Aucun document trouvé avec ce hash dans Qdrant"
                )
                
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Erreur lors de la suppression du document: {str(e)}")
            raise HTTPException(
                status_code=500,
                detail="Erreur lors de la suppression du document"
            )
    
    def find_by_hash(self, file_hash: str) -> Optional[Dict]:
        return self.document_repository.find_by_hash(file_hash)