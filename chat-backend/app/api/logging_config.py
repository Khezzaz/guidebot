import logging
import sys
from logging.handlers import RotatingFileHandler
from pathlib import Path

def setup_api_logging():
    """Configure le logging pour toute l'API"""
    
    # Créer le dossier de logs s'il n'existe pas
    log_dir = Path("logs")
    log_dir.mkdir(exist_ok=True)
    
    # Format des logs
    log_format = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # Logger principal
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    
    # Handler console (UTF-8)
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(log_format)
    
    # Handler fichier avec rotation (UTF-8)
    file_handler = RotatingFileHandler(
        log_dir / "api.log",
        maxBytes=10*1024*1024,
        backupCount=5,
        encoding="utf-8"  # ⚡ important
    )
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(log_format)
    
    # Handler pour erreurs
    error_handler = RotatingFileHandler(
        log_dir / "errors.log",
        maxBytes=10*1024*1024,
        backupCount=5,
        encoding="utf-8"  # ⚡ important
    )
    error_handler.setLevel(logging.ERROR)
    error_handler.setFormatter(log_format)
    
    # Ajouter les handlers
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)
    logger.addHandler(error_handler)
    
    # Configurer les loggers spécifiques
    uvicorn_logger = logging.getLogger("uvicorn")
    uvicorn_logger.handlers = []
    uvicorn_logger.addHandler(console_handler)
    
    fastapi_logger = logging.getLogger("fastapi")
    fastapi_logger.handlers = []
    fastapi_logger.addHandler(file_handler)
    
    return logger
