from fastapi import APIRouter, HTTPException, Depends
from app.schemas.inventory_schema import InventoryItem
from app.services.inventory_service import InventoryService
from app.utils.auth import get_current_user

router = APIRouter()
service = InventoryService()


@router.get("/")
def list_inventory(current_user=Depends(get_current_user)):
    return service.list_items()


@router.get("/{item_id}")
def get_item(item_id: int, current_user=Depends(get_current_user)):
    item = service.get_item(item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    return item


@router.post("/")
def create_item(data: InventoryItem, current_user=Depends(get_current_user)):
    return service.create_item(data)


@router.delete("/{item_id}")
def delete_item(item_id: int, current_user=Depends(get_current_user)):
    deleted = service.delete_item(item_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Item not found")
    return {"status": "deleted"}
