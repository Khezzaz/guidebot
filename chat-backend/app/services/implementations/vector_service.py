from typing import List, Optional
import logging

from app.services.interfaces.vector_interface import VectorInterface
from app.persistence.interfaces.vector_repository import AbstractVectorRepository
from app.models.qdrant_dto import QdrantDocumentInput
from app.models.documents import Document
from qdrant_client.http import models
from app.core.embedding import embed_model

logger = logging.getLogger(__name__)

class QdrantVectorService(VectorInterface):
    def __init__(self, vector_repository: AbstractVectorRepository):
        self.vector_repository = vector_repository
        self.embed_model = embed_model
    
    def add_documents(self, documents: List[QdrantDocumentInput]) -> None:
        try:
            self.vector_repository.add_documents(documents)
        except Exception as e:
            logger.error(f"Erreur lors de l'ajout des documents: {str(e)}")
            raise
    
    def semantic_search(self, query_vector: List[float], top_k: int = 5, 
                       filter: Optional[models.Filter] = None) -> List[Document]:
        try:
            return self.vector_repository.semantic_search(query_vector, top_k, filter)
        except Exception as e:
            logger.error(f"Erreur lors de la recherche sémantique: {str(e)}")
            raise
    
    def semantic_search_with_expansion(self, query_vector: List[float], 
                                     top_k: int = 5, 
                                     filter: Optional[models.Filter] = None) -> List[Document]:
        try:
            return self.vector_repository.semantic_search_with_expansion(query_vector, top_k, filter)
        except Exception as e:
            logger.error(f"Erreur lors de la recherche avec expansion: {str(e)}")
            raise
    
    def delete_document(self, file_hash: str) -> bool:
        try:
            return self.vector_repository.delete_document(file_hash)
        except Exception as e:
            logger.error(f"Erreur lors de la suppression du document: {str(e)}")
            raise
    
    def get_text_embedding(self, text: str) -> List[float]:
        try:
            return self.embed_model.get_text_embedding(text)
        except Exception as e:
            logger.error(f"Erreur lors de la génération de l'embedding: {str(e)}")
            raise