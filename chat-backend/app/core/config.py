import os
from pathlib import Path
import torch

# ——— HuggingFace —————————————————————————————————————
HF_TOKEN = os.getenv(
    "HF_TOKEN",
    "***"
)
MODEL_HF_NAME = os.getenv(
    "MODEL_HF_NAME",
    "openai/gpt-oss-20b"  
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
BASE_DIR = Path(__file__).resolve().parent.parent  # Racine du projet

UPLOAD_DIR = Path(os.getenv("UPLOAD_DIR", BASE_DIR / "app/documents/uploaded"))
CACHE_DIR = Path(os.getenv("TRANSFORMERS_CACHE", BASE_DIR / "cache"))

# ——— Modèles LLM ————————————————————————————————
GPT_OSS_MODEL_PATH = Path(os.getenv("GPT_OSS_MODEL_PATH", BASE_DIR / "llms_models/gpt-oss-20b"))
GPT2_MODEL_PATH = Path(os.getenv("GPT2_MODEL_PATH", BASE_DIR / "llms_models/gpt2"))

# ——— Device ——————————————————————————————————————
DEVICE = "cuda" if torch.cuda.is_available() else "cpu"
MAX_LENGTH = int(os.getenv("MAX_LENGTH", "4096"))

# Configuration GPU
if DEVICE == "cuda":
    GPU_MEMORY_FRACTION = float(os.getenv("GPU_MEMORY_FRACTION", "0.8"))
    torch.cuda.set_per_process_memory_fraction(GPU_MEMORY_FRACTION)

# Variables d'environnement pour Transformers
os.environ["TRANSFORMERS_CACHE"] = str(CACHE_DIR)

# ——— Debug / affichage —————————————————————————————
print(f"Configuration chargée:")
print(f"- ENVIRONMENT: {ENVIRONMENT}")
print(f"- MODEL_PATH GPT-OSS: {GPT_OSS_MODEL_PATH}")
print(f"- MODEL_PATH GPT2: {GPT2_MODEL_PATH}")
print(f"- MODEL_HF_NAME: {MODEL_HF_NAME}")
print(f"- DEVICE: {DEVICE}")
print(f"- MAX_LENGTH: {MAX_LENGTH}")
if DEVICE == "cuda":
    print(f"- GPU Memory Fraction: {GPU_MEMORY_FRACTION}")
    print(f"- CUDA Available: {torch.cuda.is_available()}")
    print(f"- GPU Count: {torch.cuda.device_count()}")
    print(f"- Current GPU: {torch.cuda.current_device()}")
    print(f"- GPU Name: {torch.cuda.get_device_name()}")
