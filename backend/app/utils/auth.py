from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import JWTError, jwt
from app.utils.security import SECRET_KEY, ALGORITHM

security = HTTPBearer()


def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """
    Validate JWT token and return current user data
    """
    token = credentials.credentials
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        user_id: int = payload.get("id")
        role: str = payload.get("role")
        
        if username is None or user_id is None:
            raise credentials_exception
            
        return {
            "id": user_id,
            "username": username,
            "role": role
        }
    except JWTError:
        raise credentials_exception


def require_role(required_role: str):
    """
    Dependency to require specific role
    """
    def verify(current_user=Depends(get_current_user)):
        if current_user.get("role") != required_role:
            raise HTTPException(
                status_code=403,
                detail=f"User lacks required role: {required_role}"
            )
        return current_user
    return verify