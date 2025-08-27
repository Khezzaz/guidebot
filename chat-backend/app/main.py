from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from datetime import datetime
import os
import logging

from app.api.routes import auth_router, document_router, query_router
from app.api.logging_config import setup_api_logging
from app.core.config import ENVIRONMENT , ALLOWED_ORIGINS
from app.services.startup_service import startup_service 

# Configuration des logs
setup_api_logging()
logger = logging.getLogger(__name__)

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

# ✅ Initialisation des services au démarrage
@app.on_event("startup")
async def startup_event():
    logger.info("Initialisation des services...")
    await startup_service.initialize_services()
    logger.info("✅ Services prêts !")

# (Optionnel) Libérer les ressources à l'arrêt
@app.on_event("shutdown")
async def shutdown_event():
    logger.info("Arrêt de l'application, libération des ressources...")
    # Ici tu peux ajouter une méthode dans StartupService pour libérer GPU/mémoire si besoin

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
        "status": "healthy" if startup_service.is_ready() else "initializing",
        "version": "1.0.0",
        "timestamp": datetime.utcnow().isoformat()
    }
