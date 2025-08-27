# app/api/routes/query.py
from fastapi import APIRouter, HTTPException, status, Depends
import logging
import time

from app.api.schemas.query import (
    QueryRequest, QueryResponse, SearchResult, 
    RetrievedChunk, SuggestionsResponse
)
from app.api.deps import get_services, optional_auth
from app.services.application_facade import ApplicationFacade

router = APIRouter(prefix="/search", tags=["Search & RAG"])
logger = logging.getLogger(__name__)

@router.post("/query",
             response_model=QueryResponse,
             summary="Question avec RAG",
             description="Pose une question et obtient une réponse générée avec contexte")
async def query_with_rag(
    request: QueryRequest,
    services: ApplicationFacade = Depends(get_services),
    current_user: dict = Depends(optional_auth)
):
    """
    Recherche sémantique + génération de réponse (RAG complet)
    """
    start_time = time.time()
    
    try:
        logger.info(f"Requête RAG: '{request.question[:50]}...'")
        
        result = services.search_and_generate_answer(
            question=request.question,
            top_k=request.top_k
        )
        
        processing_time = time.time() - start_time
        
        return QueryResponse(
            question=result["question"],
            answer=result["answer"],
            sources_count=result["sources_count"],
            chunks_used=result["chunks_used"],
            processing_time=processing_time
        )
        
    except Exception as e:
        logger.error(f"Erreur lors de la requête RAG: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erreur lors du traitement de la requête"
        )

@router.post("/semantic",
             response_model=SearchResult,
             summary="Recherche sémantique pure",
             description="Effectue uniquement une recherche sémantique sans génération")
async def semantic_search(
    request: QueryRequest,
    services: ApplicationFacade = Depends(get_services),
    current_user: dict = Depends(optional_auth)
):
    """
    Recherche sémantique sans génération de réponse
    """
    try:
        logger.info(f"Recherche sémantique: '{request.question[:50]}...'")
        
        results = services.semantic_search_only(
            question=request.question,
            top_k=request.top_k
        )
        
        # Conversion en schémas Pydantic
        retrieved_chunks = [
            RetrievedChunk(
                text=result["text"],
                metadata=result["metadata"],
                score=result.get("score"),
                chunk_index=result["metadata"].get("chunk_index"),
                source_file=result["metadata"].get("filename")
            )
            for result in results
        ]
        
        return SearchResult(
            results=retrieved_chunks,
            total_found=len(retrieved_chunks),
            query_vector_dim=768  # Dimension par défaut des embeddings
        )
        
    except Exception as e:
        logger.error(f"Erreur lors de la recherche sémantique: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erreur lors de la recherche"
        )

@router.get("/suggestions",
            response_model=SuggestionsResponse,
            summary="Suggestions de questions",
            description="Génère des suggestions de questions basées sur les documents")
async def get_suggestions(
    services: ApplicationFacade = Depends(get_services)
):
    """
    Génère des suggestions de questions
    """
    try:
        # Suggestions statiques pour l'exemple
        # Vous pourriez implémenter une logique plus sophistiquée
        suggestions = [
            "Comment procéder à l'installation ?",
            "Quelles sont les étapes de configuration ?",
            "Comment résoudre les problèmes courants ?",
            "Quels sont les prérequis système ?",
            "Comment effectuer la maintenance ?"
        ]
        
        return SuggestionsResponse(
            suggestions=suggestions,
            based_on="documents_analysis"
        )
        
    except Exception as e:
        logger.error(f"Erreur lors de la génération de suggestions: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erreur lors de la génération de suggestions"
        )

@router.get("/stats",
            summary="Statistiques de recherche",
            description="Récupère les statistiques d'utilisation de la recherche")
async def get_search_stats(
    current_user: dict = Depends(optional_auth),
    services: ApplicationFacade = Depends(get_services)
):
    """
    Statistiques d'utilisation de la recherche
    """
    try:
        # Exemple de statistiques - à implémenter selon vos besoins
        stats = {
            "total_queries": 0,  # À récupérer depuis une base de données
            "avg_processing_time": 0.0,
            "most_common_topics": [],
            "documents_indexed": len(services.get_all_documents())
        }
        
        return stats
        
    except Exception as e:
        logger.error(f"Erreur lors de la récupération des stats: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erreur lors de la récupération des statistiques"
        )