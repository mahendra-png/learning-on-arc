from fastapi import FastAPI
from pydantic import BaseModel
from typing import List

app = FastAPI()

#fake database
items = []

class Item(BaseModel):
    id: int
    name: str
    description: str
    price: float
    tax: float = None

#Read all items
@app.get("/items/", response_model=List[Item])
def get_items():
    return items

#Read a single item by name
@app.get('/items/{item_id}', response_model=Item)
def get_item(item_id: int):
    for item in items:
        if item.id == item_id:
            return item
        
    return {"error": "Item not found"}
        
#create a new item
@app.post("/items/", response_model=Item)
def create_item(item: Item):
    items.append(item)
    return item


#update an existing item
@app.put("/items/{item_id}", response_model=Item)
def update_item(item_id: int, updated_item: Item):
    for index, item in enumerate(items):
        if item.id == item_id:
            items[index] = updated_item
            return updated_item
        
    return {"error": "Item not found"}

#delete an item
@app.delete("/items/{item_id}")
def delete_item(item_id: int):
    for index, item in enumerate(items):
        if item.id == item_id:
            del items[index]
            return {"message": "Item deleted successfully"}
        
    return {"error": "Item not found"}