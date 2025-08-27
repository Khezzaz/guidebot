import bcrypt
from app.models.Admin import Admin
from app.persistence.mongodb.admin_repository import AdminMongoRepository
from app.persistence.clients.mongodb_client import init_mongo_connection

def initialize_admin():
    init_mongo_connection()

    handler = AdminMongoRepository()
    username = "othmane"

    if handler.find_by_username(username):
        print("[Init] ✅ Admin already exists. Skipping initialization.")
        return

    plain_password = "securePassword123"

    # Hash du mot de passe avec bcrypt
    hashed = bcrypt.hashpw(plain_password.encode(), bcrypt.gensalt()).decode()

    admin = Admin(
        username=username,
        password_hash=hashed,  
        role="admin"
    )

    inserted_id = handler.insert_admin(admin)
    print(f"[Init] ✅ Admin created with ID: {inserted_id}")

if __name__ == "__main__":
    initialize_admin()
