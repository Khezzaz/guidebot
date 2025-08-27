from abc import ABC, abstractmethod
from typing import Optional, Dict

class AdminInterface(ABC):
    @abstractmethod
    def authenticate(self, username: str, password: str) -> Dict:
        """Authentifie un utilisateur et retourne un token"""
        pass
    
    @abstractmethod
    def find_by_username(self, username: str) -> Optional[Dict]:
        """Trouve un admin par son nom d'utilisateur"""
        pass
    
    @abstractmethod
    def validate_token(self, token: str) -> Optional[Dict]:
        """Valide un token et retourne les informations utilisateur"""
        pass