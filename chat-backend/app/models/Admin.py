from dataclasses import dataclass
from typing import Dict, Any

@dataclass
class Admin:
    username: str
    password_hash: str
    role: str