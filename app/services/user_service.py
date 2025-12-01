from app.utils.security import hash_password, verify_password

fake_user = {
    "id": 1,
    "username": "admin",
    "email": "admin@example.com",
    "password": hash_password("admin123"),
    "role": "admin"
}


class UserService:
    def authenticate(self, username: str, password: str):
        if username != fake_user["username"]:
            return None
        if not verify_password(password, fake_user["password"]):
            return None
        return fake_user
