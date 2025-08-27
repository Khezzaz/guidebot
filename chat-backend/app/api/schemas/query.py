# app/api/schemas/query.py
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any

class QueryRequest(BaseModel):
    question: str = Field(..., min_length=1, description="Question posée")
    top_k: Optional[int] = Field(default=3, ge=1, le=20, description="Nombre de documents à récupérer")
    filters: Optional[Dict[str, Any]] = Field(None, description="Filtres optionnels")

class RetrievedChunk(BaseModel):
    text: str = Field(..., description="Contenu textuel du chunk")
    metadata: Dict[str, Any] = Field(..., description="Métadonnées du chunk")
    score: Optional[float] = Field(None, description="Score de similarité")
    chunk_index: Optional[int] = Field(None, description="Index du chunk dans le document")
    source_file: Optional[str] = Field(None, description="Fichier source")

class QueryResponse(BaseModel):
    question: str = Field(..., description="Question originale")
    answer: str = Field(..., description="Réponse générée")
    sources_count: int = Field(..., description="Nombre de sources utilisées")
    chunks_used: List[str] = Field(default_factory=list, description="Aperçu des chunks utilisés")
    processing_time: Optional[float] = Field(None, description="Temps de traitement en secondes")

class SearchResult(BaseModel):
    results: List[RetrievedChunk] = Field(..., description="Résultats de la recherche")
    total_found: int = Field(..., description="Nombre total de résultats trouvés")
    query_vector_dim: Optional[int] = Field(None, description="Dimension du vecteur de requête")

class SuggestionsResponse(BaseModel):
    suggestions: List[str] = Field(..., description="Suggestions de questions")
    based_on: str = Field(..., description="Base utilisée pour les suggestions")

