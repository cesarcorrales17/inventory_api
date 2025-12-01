from typing import List, Optional
from app.schemas.inventory_schema import InventoryItem, InventoryItemCreate

# In-memory storage for demo purposes
# In production, replace with database operations
inventory_db = {}
next_id = 1


class InventoryService:
    def list_items(self) -> List[InventoryItem]:
        """Return all inventory items"""
        return list(inventory_db.values())
    
    def get_item(self, item_id: int) -> Optional[InventoryItem]:
        """Get a specific item by ID"""
        return inventory_db.get(item_id)
    
    def create_item(self, data: InventoryItemCreate) -> InventoryItem:
        """Create a new inventory item"""
        global next_id
        
        # Create new item with auto-generated ID
        new_item = InventoryItem(
            id=next_id,
            name=data.name,
            quantity=data.quantity,
            price=data.price,
            description=data.description
        )
        
        inventory_db[next_id] = new_item
        next_id += 1
        
        return new_item
    
    def update_item(self, item_id: int, data: InventoryItemCreate) -> Optional[InventoryItem]:
        """Update an existing item"""
        if item_id not in inventory_db:
            return None
        
        updated_item = InventoryItem(
            id=item_id,
            name=data.name,
            quantity=data.quantity,
            price=data.price,
            description=data.description
        )
        
        inventory_db[item_id] = updated_item
        return updated_item
    
    def delete_item(self, item_id: int) -> bool:
        """Delete an item"""
        if item_id in inventory_db:
            del inventory_db[item_id]
            return True
        return False