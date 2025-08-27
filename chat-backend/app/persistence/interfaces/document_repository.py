from abc import ABC , abstractmethod
from typing import List , Optional
from app.models.pdf_metadata import PDFMetadata

class AbstractDocumentRepository(ABC):
    @abstractmethod
    def insert_pdf_metadata(self, metadata: PDFMetadata) -> str:
        pass
    @abstractmethod
    def find_by_hash(self, file_hash: str) -> Optional[dict]:
        pass
    @abstractmethod
    def list_documents(self, limit: int = 100) -> list[PDFMetadata]:
        pass
    @abstractmethod
    def delete_by_hash(self, file_hash: str) -> bool:
        pass