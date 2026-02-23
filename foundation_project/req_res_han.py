from fastapi import FastAPI
from pydantic import BaseModel, Field

app = FastAPI()

class Item(BaseModel):
    name: str = Field(..., min_length=3, max_length=50)
    price: float = Field(..., gt=0)
    tax: float | None = Field(default=None, ge=0)


@app.post("/items/")
def create_item(item: Item):
    return item
