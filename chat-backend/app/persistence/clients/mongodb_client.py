#mongodb_client.py
from pymongo import MongoClient
from app.core.config import MONGODB_URI, MONGODB_DB_NAME , MONGODB_COLLECTIONS

# Initialisation du client MongoDB
client = MongoClient(MONGODB_URI)

# Accès à la base de données par défaut
db = client[MONGODB_DB_NAME]

def get_mongo_client() -> MongoClient:
    """Retourne le client MongoDB."""
    return client

def get_mongo_db():
    """Retourne la base MongoDB utilisée."""
    return db

def get_collection(collectionname: str = None):
    if collectionname:
        return db[MONGODB_COLLECTIONS[collectionname]]
    return db[MONGODB_COLLECTIONS["documents"]]

def init_mongo_connection():
    """Teste la connexion MongoDB."""
    try:
        client.admin.command('ping')
        print(f"[MongoDB] ✅ Connected successfully to {MONGODB_URI}")
    except Exception as e:
        print(f"[MongoDB] ❌ Connection failed: {e}")
