# app.py
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict

app = FastAPI(title="ShopEasy Inventory Management Service")

# Mock Database
inventory_db: Dict[int, dict] = {
    1: {"name": "Wireless Headphones", "price": 2999.00, "stock": 50},
    2: {"name": "Casual Slim Fit Shirt", "price": 1299.00, "stock": 120}
}

class Product(BaseModel):
    name: str
    price: float
    stock: int

@app.get("/")
def health_check():
    return {"status": "healthy", "service": "inventory-management"}

@app.get("/products/{product_id}")
def check_stock(product_id: int):
    if product_id not in inventory_db:
        raise HTTPException(status_code=404, detail="Product not found")
    return inventory_db[product_id]

@app.post("/products/{product_id}")
def add_or_update_product(product_id: int, product: Product):
    inventory_db[product_id] = product.dict()
    return {"message": "Product successfully updated", "data": inventory_db[product_id]}