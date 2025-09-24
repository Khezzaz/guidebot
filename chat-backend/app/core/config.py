# app/core/config.py

import os
import torch

# ——— HuggingFace —————————————————————————————————————
HF_TOKEN = os.getenv(
    "HF_TOKEN",
    "ajoutez ici !!!"
)

# ——— Qdrant ————————————————————————————————————————
QDRANT_HOST = os.getenv("QDRANT_HOST", "http://localhost:6333")
QDRANT_PORT = int(os.getenv("QDRANT_PORT", "6333"))
QDRANT_COLLECTION_NAME = os.getenv("QDRANT_COLLECTION", "documents")
VECTOR_SIZE = int(os.getenv("VECTOR_SIZE", "384"))

# ——— MongoDB ———————————————————————————————————————
MONGODB_URI = os.getenv("MONGODB_URI", "mongodb://localhost:27017")
MONGODB_DB_NAME = os.getenv("MONGODB_DB_NAME", "snrt-documents")
MONGODB_COLLECTIONS = {
    "documents": os.getenv("MONGODB_COLLECTION_DOCUMENTS", "vectorized-documents"),
    "admins":    os.getenv("MONGODB_COLLECTION_ADMINS",    "admins")
}

# ——— Environnement & CORS —————————————————————————————
ENVIRONMENT = os.getenv("ENVIRONMENT", "development")
ALLOWED_ORIGINS = os.getenv(
    "ALLOWED_ORIGINS",
    "http://localhost:3000"
).split(",")

# ——— Autres chemins ———————————————————————————————————
UPLOAD_DIR = os.getenv("UPLOAD_DIR", "app/documents/uploaded")

MODEL_PATH = os.getenv("MODEL_PATH", "./models/gpt-oss-20b")  # Chemin vers votre modèle local
DEVICE = "cuda" if torch.cuda.is_available() else "cpu"
MAX_LENGTH = int(os.getenv("MAX_LENGTH", "4096"))

# Configuration GPU
if DEVICE == "cuda":
    GPU_MEMORY_FRACTION = float(os.getenv("GPU_MEMORY_FRACTION", "0.8"))
    torch.cuda.set_per_process_memory_fraction(GPU_MEMORY_FRACTION)

# Configuration de cache pour les modèles
TRANSFORMERS_CACHE = os.getenv("TRANSFORMERS_CACHE", "./cache")
os.environ["TRANSFORMERS_CACHE"] = TRANSFORMERS_CACHE
