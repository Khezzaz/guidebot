from app.persistence.interfaces.vector_repository import AbstractVectorRepository
from typing import List, Optional
from qdrant_client.http import models
from app.core.config import QDRANT_COLLECTION_NAME, VECTOR_SIZE
from app.persistence.clients.qdrant_client import get_qdrant_client, init_qdrant_collection
from app.models.qdrant_dto import QdrantDocumentInput
from app.models.documents import Document
import logging

logger = logging.getLogger(__name__)


class VectorQdrantRepository(AbstractVectorRepository):
    def __init__(self):
        self.client = get_qdrant_client()
        init_qdrant_collection(VectorSize=VECTOR_SIZE)

    def add_documents(self, documents: List[QdrantDocumentInput]) -> None:
        points = [
            models.PointStruct(
                id=doc.id,
                vector=doc.embedding,
                payload={
                    "content": doc.content,
                    **doc.metadata
                }
            ) for doc in documents
        ]

        self.client.upsert(
            collection_name=QDRANT_COLLECTION_NAME,
            points=points
        )

    def semantic_search(
        self,
        query_vector: List[float],
        top_k: int = 5,
        filter: Optional[models.Filter] = None,
    ) -> List[Document]:
        results = self.client.search(
            collection_name=QDRANT_COLLECTION_NAME,
            query_vector=query_vector,
            limit=top_k,
            query_filter=filter,
            search_params=models.SearchParams(hnsw_ef=128),
        )
        return [
            Document(
                id=str(r.id),
                text=r.payload.get("content", ""),
                metadata={k: v for k, v in r.payload.items() if k != "content"},
            ) for r in results
        ]

    def semantic_search_with_expansion(
        self,
        query_vector: List[float],
        top_k: int = 5,
        filter: Optional[models.Filter] = None,
    ) -> List[Document]:
        logger.info(f"Starting semantic_search_with_expansion(top_k={top_k}, filter={filter})")
        main_results = self.semantic_search(query_vector, top_k=top_k, filter=filter)
        logger.debug(f"Found {len(main_results)} main results")

        expanded_results: List[Document] = []
        seen_ids = set()

        for doc in main_results:
            expanded_results.append(doc)
            seen_ids.add(doc.id)

            file_hash = doc.metadata.get("doc_hash")
            chunk_index = doc.metadata.get("chunk_index")
            logger.debug(f"Processing doc id={doc.id}, hash={file_hash}, index={chunk_index}")

            if file_hash is None or chunk_index is None:
                logger.warning(f"Skipping expansion for doc id={doc.id} due to missing metadata")
                continue

            for neighbor_index in (chunk_index - 1, chunk_index + 1):
                logger.debug(f"Looking for neighbor at index={neighbor_index}")
                neighbor_filter = models.Filter(
                    must=[
                        models.FieldCondition(
                            key="doc_hash",
                            match=models.MatchValue(value=file_hash)
                        ),
                        models.FieldCondition(
                            key="chunk_index",
                            match=models.MatchValue(value=neighbor_index)
                        )
                    ]
                )
                neighbors = self.semantic_search(query_vector, top_k=1, filter=neighbor_filter)
                if neighbors:
                    neighbor = neighbors[0]
                    if neighbor.id not in seen_ids:
                        expanded_results.append(neighbor)
                        seen_ids.add(neighbor.id)
                        logger.info(f"Added neighbor id={neighbor.id} at index={neighbor_index}")
                    else:
                        logger.debug(f"Neighbor id={neighbor.id} already seen, skipping")
                else:
                    logger.debug(f"No neighbor found at index={neighbor_index}")

        logger.info(f"Expansion complete: total results = {len(expanded_results)}")
        return expanded_results
    
    def delete_document(self, file_hash: str) -> bool:
        """
        Supprime tous les documents ayant le file_hash spécifié
        et vérifie s'ils ont bien été supprimés.
        """
        delete_filter = models.Filter(
            must=[
                models.FieldCondition(
                    key="file_hash",
                    match=models.MatchValue(value=file_hash)
                )
            ]
        )

        # Suppression
        self.client.delete(
            collection_name=QDRANT_COLLECTION_NAME,
            points_selector=models.FilterSelector(filter=delete_filter)
        )

        # Vérification via scroll
        remaining = self.client.scroll(
            collection_name=QDRANT_COLLECTION_NAME,
            scroll_filter=delete_filter,
            limit=1
        )

        return len(remaining[0]) == 0  