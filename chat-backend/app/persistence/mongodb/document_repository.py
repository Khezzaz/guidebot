from app.persistence.interfaces.document_repository import AbstractDocumentRepository
from pymongo.collection import Collection
from app.models.pdf_metadata import PDFMetadata
from app.persistence.clients.mongodb_client import  get_collection
from typing import Optional
from dataclasses import asdict

class DocumentMongoRepository(AbstractDocumentRepository):
    
    def __init__(self):
        self.collection: Collection = get_collection(collectionname="documents")

    def insert_pdf_metadata(self, metadata: PDFMetadata) -> str:
        result = self.collection.insert_one(asdict(metadata))
        return str(result.inserted_id)

    def find_by_hash(self, file_hash: str) -> Optional[dict]:
        return self.collection.find_one({"file_hash": file_hash})

    def list_documents(self, limit: int = 100) -> list[PDFMetadata]:
        return list(self.collection.find().sort("created_at", -1).limit(limit))

    def delete_by_hash(self, file_hash: str) -> bool:
        result = self.collection.delete_one({"file_hash": file_hash})
        return result.deleted_count > 0