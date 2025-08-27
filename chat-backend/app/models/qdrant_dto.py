from dataclasses import dataclass
from typing import Dict, Any, List

@dataclass
class QdrantDocumentInput:
    id: str
    content: str
    metadata: Dict[str, Any]
    embedding: List[float]