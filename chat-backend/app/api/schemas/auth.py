# app/api/schemas/auth.py
from pydantic import BaseModel, Field
from typing import Optional

class LoginRequest(BaseModel):
    username: str = Field(..., min_length=1, description="Nom d'utilisateur")
    password: str = Field(..., min_length=1, description="Mot de passe")

class TokenResponse(BaseModel):
    access_token: str = Field(..., description="Token d'accès JWT")
    token_type: str = Field(default="bearer", description="Type de token")
    expires_in: int = Field(..., description="Durée de validité en secondes")

class TokenData(BaseModel):
    username: str = Field(..., description="Nom d'utilisateur")
    role: str = Field(default="user", description="Rôle de l'utilisateur")
    sub: str = Field(..., description="Subject du token")

class RefreshTokenRequest(BaseModel):
    refresh_token: str = Field(..., description="Token de rafraîchissement")