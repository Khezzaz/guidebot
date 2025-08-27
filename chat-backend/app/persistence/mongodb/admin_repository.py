from app.persistence.interfaces.admin_repository import AbstractAdminRepository
from pymongo.collection import Collection
from app.persistence.clients.mongodb_client import get_mongo_db , get_collection
from typing import Optional
from dataclasses import asdict
from app.models.Admin import Admin

class AdminMongoRepository(AbstractAdminRepository):
    def __init__(self):
        self.collection : Collection = get_collection(collectionname="admins")

    def find_by_username(self, username: str) -> Optional[dict]:
        return self.collection.find_one({"username": username})
    
    def find_by_password(self , passwrord : str):
        return self.collection.find_one({"passwrord" :passwrord})
    
    def insert_admin(self , admin : Admin):
        result = self.collection.insert_one(asdict(admin))
        return str(result.inserted_id)