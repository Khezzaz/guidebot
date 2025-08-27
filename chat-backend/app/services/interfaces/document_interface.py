from abc import ABC, abstractmethod
from typing import List, Dict, Optional
from fastapi import UploadFile
from app.models.pdf_metadata import PDFMetadata

class DocumentInterface(ABC):
    @abstractmethod
    async def upload_and_process(self, file: UploadFile, system_name: str) -> Dict:
        """Upload, traite et vectorise un document"""
        pass
    
    @abstractmethod
    def get_all_documents(self) -> List[Dict]:
        """Récupère la liste de tous les documents"""
        pass
    
    @abstractmethod
    def delete_document(self, file_hash: str) -> Dict:
        """Supprime un document par son hash"""
        pass
    
    @abstractmethod
    def find_by_hash(self, file_hash: str) -> Optional[Dict]:
        """Trouve un document par son hash"""
        pass