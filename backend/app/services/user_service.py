from typing import Optional, List
from app.utils.security import hash_password, verify_password
from app.schemas.user_schema import User

# Fake database with demo users
fake_users_db = {
    "admin": {
        "id": 1,
        "username": "admin",
        "email": "admin@example.com",
        "password": hash_password("admin123"),
        "role": "admin"
    },
    "user": {
        "id": 2,
        "username": "user",
        "email": "user@example.com",
        "password": hash_password("user123"),
        "role": "user"
    }
}


class UserService:
    def authenticate(self, username: str, password: str) -> Optional[dict]:
        """Authenticate user with username and password"""
        user = fake_users_db.get(username)
        
        if not user:
            return None
            
        if not verify_password(password, user["password"]):
            return None
        
        # Return user without password
        return {
            "id": user["id"],
            "username": user["username"],
            "email": user["email"],
            "role": user["role"]
        }
    
    def list_users(self) -> List[User]:
        """List all users (without passwords)"""
        users = []
        for user_data in fake_users_db.values():
            users.append(User(
                id=user_data["id"],
                username=user_data["username"],
                email=user_data["email"],
                role=user_data["role"]
            ))
        return users
    
    def get_user_by_username(self, username: str) -> Optional[dict]:
        """Get user by username"""
        user = fake_users_db.get(username)
        if not user:
            return None
        
        return {
            "id": user["id"],
            "username": user["username"],
            "email": user["email"],
            "role": user["role"]
        }