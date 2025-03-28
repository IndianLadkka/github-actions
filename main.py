from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional

app = FastAPI()

# Sample data store
items_db = {
    1: {"name": "Premium Coffee", "price": 9.99, "featured": True},
    2: {"name": "Standard Tea", "price": 4.99, "featured": False},
    3: {"name": "Deluxe Chocolate", "price": 12.99, "featured": True},
}

class Item(BaseModel):
    name: str
    price: float
    featured: Optional[bool] = False

@app.get("/")
def read_root():
    return {"message": "Welcome to the Item API - check /items or /featured-items"}

@app.get("/items/")
def list_items():
    """List all items"""
    return {"items": items_db}

@app.get("/items/{item_id}")
def get_item(item_id: int):
    """Get specific item by ID"""
    if item_id not in items_db:
        return {"error": "Item not found"}
    return items_db[item_id]

@app.get("/featured-items/")
def get_featured_items():
    """Get only featured items"""
    featured = {id: item for id, item in items_db.items() if item["featured"]}
    return {"featured_items": featured}

@app.post("/items/")
def create_item(item: Item):
    """Create a new item"""
    new_id = max(items_db.keys()) + 1
    items_db[new_id] = item.dict()
    return {"message": "Item created", "item_id": new_id}

@app.put("/items/{item_id}")
def update_item(item_id: int, item: Item):
    """Update an existing item"""
    if item_id not in items_db:
        return {"error": "Item not found"}
    items_db[item_id] = item.dict()
    return {"message": "Item updated", "item_id": item_id}