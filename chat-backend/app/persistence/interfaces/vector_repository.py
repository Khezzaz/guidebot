from abc import ABC , abstractmethod
from typing import List , Optional
from app.models.qdrant_dto import QdrantDocumentInput
from app.models.documents import Document
from qdrant_client.http import models


class AbstractVectorRepository(ABC):
    @abstractmethod
    def add_documents(self, documents: List[QdrantDocumentInput]) -> None:
        pass
    def semantic_search(
        self,
        query_vector: List[float],
        top_k: int = 5,
        filter: Optional[models.Filter] = None,
    ) -> List[Document]:
        pass
    @abstractmethod
    def semantic_search_with_expansion(
        self,
        query_vector: List[float],
        top_k: int = 5,
        filter: Optional[models.Filter] = None,
    ) -> List[Document]:
        pass
    @abstractmethod
    def delete_document(self, file_hash: str) -> bool:
        pass