# app/api/schemas/document.py
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime

class UploadResponse(BaseModel):
    status: str = Field(..., description="Statut de l'opération")
    message: str = Field(..., description="Message descriptif")
    file_hash: str = Field(..., description="Hash unique du fichier")
    document_id: Optional[str] = Field(None, description="ID du document en base")

class DocumentMetadata(BaseModel):
    filename: str = Field(..., description="Nom du fichier")
    file_hash: str = Field(..., description="Hash unique du fichier")
    system_name: str = Field(..., description="Nom du système source")
    created_at: str = Field(..., description="Date de création")
    file_size: Optional[int] = Field(None, description="Taille du fichier en octets")

class DocumentListResponse(BaseModel):
    documents: List[DocumentMetadata] = Field(..., description="Liste des documents")
    total: int = Field(..., description="Nombre total de documents")
    
class DeleteResponse(BaseModel):
    status: str = Field(..., description="Statut de la suppression")
    message: str = Field(..., description="Message descriptif")
    file_hash: str = Field(..., description="Hash du fichier supprimé")

class DocumentDetailResponse(BaseModel):
    metadata: DocumentMetadata = Field(..., description="Métadonnées du document")
    chunks_count: Optional[int] = Field(None, description="Nombre de chunks vectorisés")
    last_accessed: Optional[datetime] = Field(None, description="Dernier accès")
