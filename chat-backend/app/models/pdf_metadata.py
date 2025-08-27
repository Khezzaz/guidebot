from dataclasses import dataclass, field
from datetime import datetime

@dataclass
class PDFMetadata:
    filename: str
    file_hash: str
    system_name: str
    created_at: datetime = field(default_factory=datetime.utcnow)
