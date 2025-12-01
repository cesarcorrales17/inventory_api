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
