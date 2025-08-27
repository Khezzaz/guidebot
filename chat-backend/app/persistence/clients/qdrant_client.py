#qdrant_client.py
from qdrant_client import QdrantClient
from qdrant_client.http import models
from qdrant_client.http.models import Distance , VectorParams
from app.core.config import QDRANT_COLLECTION_NAME , QDRANT_HOST , QDRANT_PORT

client = QdrantClient(url=QDRANT_HOST , port= QDRANT_PORT)

def init_qdrant_collection(VectorSize: int = 768):
    existing_collections = client.get_collections().collections
    if any(col.name == QDRANT_COLLECTION_NAME for col in existing_collections):
        print(f"[Qdrant]  Collection '{QDRANT_COLLECTION_NAME}' already exists.")
        return
    print(f"[Qdrant] ⏳ Creating collection '{QDRANT_COLLECTION_NAME}'...")

    client.recreate_collection(
        collection_name=QDRANT_COLLECTION_NAME,
        vectors_config=VectorParams(
            size=VectorSize,  
            distance=Distance.COSINE,
        ),
    )
    print(f"[Qdrant] ✅ Collection '{QDRANT_COLLECTION_NAME}' created successfully.")


def get_qdrant_client() -> QdrantClient:
    return client