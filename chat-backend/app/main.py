from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from datetime import datetime
from app.api.routes import auth_router, document_router, query_router
from app.api.logging_config import setup_api_logging
from app.core.config import ENVIRONMENT , ALLOWED_ORIGINS

# Configuration des logs
setup_api_logging()

app = FastAPI(
    title="RAG API - SNRT",
    description="API pour gestion de documents PDF, vectorisation et interrogation LLM",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Configuration CORS adaptée à l'environnement
origins = ["*"] if ENVIRONMENT == "development" else ALLOWED_ORIGINS

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)

# Inclusion des routes avec préfixes
app.include_router(auth_router)
app.include_router(document_router)
app.include_router(query_router)

# Routes utilitaires
@app.get("/")
async def root():
    return {
        "message": "Bienvenue sur l'API RAG SNRT",
        "docs": "/docs",
        "version": "1.0.0"
    }

@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "version": "1.0.0",
        "timestamp": datetime.utcnow().isoformat()
    }