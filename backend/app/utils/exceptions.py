from fastapi import HTTPException

def not_found(detail: str):
    raise HTTPException(status_code=404, detail=detail)
