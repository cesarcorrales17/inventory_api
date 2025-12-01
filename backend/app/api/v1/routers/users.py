from fastapi import APIRouter, HTTPException, Depends
from app.schemas.user_schema import User, UserLogin, Token
from app.services.user_service import UserService
from app.utils.security import create_access_token
from app.utils.auth import get_current_user

router = APIRouter()
service = UserService()


@router.post("/login", response_model=Token)
def login(data: UserLogin):
    user = service.authenticate(data.username, data.password)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid username or password")

    token = create_access_token({
        "sub": user["username"],
        "id": user["id"],
        "role": user["role"]
    })
    return Token(access_token=token)


@router.get("/me", response_model=User)
def get_current_user_info(current_user=Depends(get_current_user)):
    return User(
        id=current_user["id"],
        username=current_user["username"],
        email=current_user.get("email", ""),
        role=current_user["role"]
    )


@router.get("/", response_model=list[User])
def list_users(current_user=Depends(get_current_user)):
    """List all users (admin only in production)"""
    users = service.list_users()
    return users