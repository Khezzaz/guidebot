# app/services/startup_service.py
import logging
import sys
import asyncio
from typing import Optional
from app.services.implementations.local_llm_service import LocalLlmService

logger = logging.getLogger(__name__)

class StartupService:
    """Service responsable du chargement des ressources au démarrage de l'application."""
    
    def __init__(self):
        self.llm_service: Optional[LocalLlmService] = None
        self.startup_completed = False
    
    async def initialize_services(self):
        """Initialise tous les services qui nécessitent un chargement au démarrage."""
        try:
            logger.info("Démarrage de l'initialisation des services...")

            # Chargement du modèle LLM
            logger.info("Chargement du modèle LLM local...")
            self.llm_service = LocalLlmService()
            
            # Vérification que le modèle est bien chargé
            model_info = self.llm_service.get_model_info()
            if not model_info["model_loaded"]:
                raise RuntimeError("Le modèle LLM n'a pas pu être chargé")
            
            logger.info("Modèle LLM chargé avec succès")
            logger.info(f"   - Modèle: {model_info['model_name']}")
            logger.info(f"   - Device: {model_info['device']}")

            self.startup_completed = True
            logger.info("Initialisation des services terminée avec succès !")
            
        except Exception as e:
            logger.error(f"Erreur lors de l'initialisation des services: {str(e)}")
            raise
    
    def get_llm_service(self) -> LocalLlmService:
        """Retourne le service LLM initialisé."""
        if not self.startup_completed:
            raise RuntimeError("Les services ne sont pas encore initialisés")
        return self.llm_service
    
    def is_ready(self) -> bool:
        """Vérifie si l'application est prête à traiter les requêtes."""
        return self.startup_completed and self.llm_service is not None

# Instance globale
startup_service = StartupService()
