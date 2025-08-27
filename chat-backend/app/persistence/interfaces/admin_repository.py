from abc import ABC, abstractmethod
from typing import Optional
from app.models.Admin import Admin

class AbstractAdminRepository(ABC):
    @abstractmethod
    def find_by_username(self,username :str)-> Optional[dict]:
        pass

    @abstractmethod
    def find_by_password(self , passwrord : str):
        pass

    @abstractmethod
    def insert_admin(self , admin : Admin):
        pass