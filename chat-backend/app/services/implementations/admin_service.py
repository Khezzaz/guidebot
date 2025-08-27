from datetime import timedelta
from fastapi import HTTPException, status
import bcrypt
import logging
from typing import Optional, Dict

from app.services.interfaces.admin_interface import AdminInterface
from app.core.token_generator import create_access_token
from app.persistence.interfaces.admin_repository import AbstractAdminRepository

logger = logging.getLogger(__name__)

class JwtAdminService(AdminInterface):
    def __init__(self, admin_repository: AbstractAdminRepository):
        self.admin_repository = admin_repository
        self.access_token_expire_minutes = 30
    
    def authenticate(self, username: str, password: str) -> Dict:
        try:
            logger.info(f"Tentative de connexion pour l'utilisateur: {username}")
            
            user = self.admin_repository.find_by_username(username)
            
            if not user:
                logger.warning(f"Utilisateur non trouvé: {username}")
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED, 
                    detail="Invalid credentials"
                )
            
            logger.info(f"Utilisateur trouvé: {user.get('username', 'Unknown')}")
            
            hashed_password = user.get("password_hash")
            
            if not hashed_password:
                logger.error("Mot de passe manquant dans la base de données")
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED, 
                    detail="Invalid credentials"
                )
            
            # Conversion du hash en bytes si nécessaire
            if isinstance(hashed_password, str):
                hashed_password_bytes = hashed_password.encode('utf-8')
            elif isinstance(hashed_password, bytes):
                hashed_password_bytes = hashed_password
            else:
                logger.error(f"Type de mot de passe inattendu: {type(hashed_password)}")
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED, 
                    detail="Invalid credentials"
                )
            
            password_bytes = password.encode('utf-8')
            
            if not bcrypt.checkpw(password_bytes, hashed_password_bytes):
                logger.warning(f"Mot de passe incorrect pour l'utilisateur: {username}")
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED, 
                    detail="Invalid credentials"
                )
            
            logger.info(f"Authentification réussie pour: {username}")
            
            access_token = create_access_token(
                data={"sub": user["username"], "role": user.get("role", "admin")},
                expires_delta=timedelta(minutes=self.access_token_expire_minutes)
            )
            
            return {
                "access_token": access_token,
                "token_type": "bearer",
                "expires_in": self.access_token_expire_minutes * 60
            }
            
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Erreur inattendue lors de l'authentification: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
                detail="Internal server error"
            )
    
    def find_by_username(self, username: str) -> Optional[Dict]:
        return self.admin_repository.find_by_username(username)
    
    def validate_token(self, token: str) -> Optional[Dict]:
        # Implémentation de la validation du token
        # À implémenter selon votre logique de token
        pass
