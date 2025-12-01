from pydantic import BaseModel, Field
from typing import Optional


class InventoryItemBase(BaseModel):
    """Base schema for inventory items"""
    name: str = Field(..., min_length=1, max_length=200)
    quantity: int = Field(..., ge=0)
    price: float = Field(..., ge=0)
    description: Optional[str] = None


class InventoryItemCreate(InventoryItemBase):
    """Schema for creating inventory items (no ID)"""
    pass


class InventoryItem(InventoryItemBase):
    """Schema for inventory items with ID"""
    id: int
    
    class Config:
        from_attributes = True