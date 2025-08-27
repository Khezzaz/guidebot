from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
import logging

from app.api.schemas.auth import LoginRequest, TokenResponse, TokenData
from app.api.deps import get_services, get_current_user
from app.services.application_facade import ApplicationFacade

router = APIRouter(prefix="/auth", tags=["Authentication"])
logger = logging.getLogger(__name__)
security = HTTPBearer()

@router.post("/login", 
             response_model=TokenResponse,
             summary="Authentification utilisateur",
             description="Authentifie un utilisateur et retourne un token JWT")
async def login(
    request: LoginRequest,
    services: ApplicationFacade = Depends(get_services)
):
    """
    Authentifie un utilisateur avec username/password
    """
    try:
        logger.info(f"Tentative de connexion pour: {request.username}")
        
        result = services.login(request.username, request.password)
        
        logger.info(f"Connexion réussie pour: {request.username}")
        
        return TokenResponse(
            access_token=result["access_token"],
            token_type=result["token_type"],
            expires_in=result.get("expires_in", 1800)
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Erreur lors de la connexion: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erreur interne du serveur"
        )

@router.get("/me",
            response_model=TokenData,
            summary="Informations utilisateur actuel",
            description="Récupère les informations de l'utilisateur connecté")
async def get_current_user_info(
    current_user: dict = Depends(get_current_user)
):
    """
    Retourne les informations de l'utilisateur actuellement connecté
    """
    return TokenData(
        username=current_user.get("sub", "unknown"),
        role=current_user.get("role", "user"),
        sub=current_user.get("sub", "unknown")
    )

@router.post("/logout",
             summary="Déconnexion",
             description="Déconnecte l'utilisateur (côté client)")
async def logout():
    """
    Endpoint pour la déconnexion (principalement côté client)
    """
    return {"message": "Déconnexion réussie"}

@router.post("/validate-token",
             summary="Validation de token",
             description="Valide un token JWT")
async def validate_token(
    current_user: dict = Depends(get_current_user)
):
    """
    Valide le token fourni
    """
    return {
        "valid": True,
        "user": current_user.get("sub"),
        "role": current_user.get("role")
    }
