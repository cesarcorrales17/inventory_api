from fastapi import APIRouter, HTTPException, Depends
from typing import List
from app.schemas.inventory_schema import InventoryItem, InventoryItemCreate
from app.services.inventory_service import InventoryService
from app.utils.auth import get_current_user

router = APIRouter()
service = InventoryService()


@router.get("/", response_model=List[InventoryItem])
def list_inventory(current_user=Depends(get_current_user)):
    """Get all inventory items"""
    return service.list_items()


@router.get("/{item_id}", response_model=InventoryItem)
def get_item(item_id: int, current_user=Depends(get_current_user)):
    """Get a specific inventory item by ID"""
    item = service.get_item(item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    return item


@router.post("/", response_model=InventoryItem)
def create_item(data: InventoryItemCreate, current_user=Depends(get_current_user)):
    """Create a new inventory item"""
    return service.create_item(data)


@router.put("/{item_id}", response_model=InventoryItem)
def update_item(item_id: int, data: InventoryItemCreate, current_user=Depends(get_current_user)):
    """Update an existing inventory item"""
    item = service.update_item(item_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    return item


@router.delete("/{item_id}")
def delete_item(item_id: int, current_user=Depends(get_current_user)):
    """Delete an inventory item"""
    deleted = service.delete_item(item_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Item not found")
    return {"status": "deleted", "id": item_id}