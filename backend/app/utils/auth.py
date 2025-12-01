def require_role(required_role: str):
    def verify(current_user=Depends(get_current_user)):
        if current_user.get("role") != required_role:
            raise HTTPException(
                status_code=403,
                detail=f"User lacks required role: {required_role}"
            )
        return current_user
    return verify
