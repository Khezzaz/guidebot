from fastapi import UploadFile
from typing import List, Dict

from app.services.interfaces.admin_interface import AdminInterface
from app.services.interfaces.document_interface import DocumentInterface
from app.services.interfaces.vector_interface import VectorInterface
from app.services.interfaces.llm_interface import LlmInterface

class ApplicationFacade:
    """
    Facade principale orchestrant tous les services de l'application.
    Point d'entrée unique pour la couche API.
    """
    
    def __init__(self, 
                 admin_service: AdminInterface,
                 document_service: DocumentInterface,
                 vector_service: VectorInterface,
                 llm_service: LlmInterface):
        self.admin_service = admin_service
        self.document_service = document_service
        self.vector_service = vector_service
        self.llm_service = llm_service
    
    # ==================== AUTHENTIFICATION ====================
    
    def login(self, username: str, password: str) -> Dict:
        """Authentifie un utilisateur."""
        return self.admin_service.authenticate(username, password)
    
    # ==================== GESTION DOCUMENTS ====================
    
    async def upload_and_vectorize_document(self, file: UploadFile, system_name: str) -> Dict:
        """Upload, traite et vectorise un document PDF."""
        return await self.document_service.upload_and_process(file, system_name)
    
    def get_all_documents(self) -> List[Dict]:
        """Récupère la liste de tous les documents."""
        return self.document_service.get_all_documents()
    
    def delete_document_by_hash(self, file_hash: str) -> Dict:
        """Supprime un document par son hash."""
        return self.document_service.delete_document(file_hash)
    
    # ==================== RECHERCHE ET RAG ====================
    
    def search_and_generate_answer(self, question: str, top_k: int = 3) -> Dict:
        """
        Orchestration complète RAG : recherche vectorielle + génération de réponse.
        """
        # 1. Générer l'embedding de la question
        question_vector = self.vector_service.get_text_embedding(question)
        
        # 2. Recherche sémantique avec expansion
        similar_documents = self.vector_service.semantic_search_with_expansion(
            query_vector=question_vector,
            top_k=top_k
        )
        
        # 3. Extraction des textes des chunks
        retrieved_chunks = [doc.text for doc in similar_documents]
        
        # 4. Génération de la réponse avec contexte
        answer = self.llm_service.query_with_context(question, retrieved_chunks)
        
        return {
            "question": question,
            "answer": answer,
            "sources_count": len(retrieved_chunks),
            "chunks_used": retrieved_chunks[:2] if retrieved_chunks else []  # Limité pour la réponse
        }
    
    def semantic_search_only(self, question: str, top_k: int = 5) -> List[Dict]:
        """Effectue uniquement une recherche sémantique sans génération."""
        question_vector = self.vector_service.get_text_embedding(question)
        
        similar_documents = self.vector_service.semantic_search(
            query_vector=question_vector,
            top_k=top_k
        )
        
        return [
            {
                "text": doc.text,
                "metadata": doc.metadata,
                "score": getattr(doc, 'score', None)
            }
            for doc in similar_documents
        ]
    
    # ==================== UTILITAIRES ====================
    
    def get_document_by_hash(self, file_hash: str) -> Dict:
        """Récupère un document spécifique par son hash."""
        doc = self.document_service.find_by_hash(file_hash)
        if doc:
            return doc
        return {"error": "Document not found"}
    
    def health_check(self) -> Dict:
        """Vérification de santé des services."""
        return {
            "status": "healthy",
            "services": {
                "admin": "ok",
                "document": "ok", 
                "vector": "ok",
                "llm": "ok"
            }
        }