from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from typing import List, Optional
import time

app = FastAPI()

# Data Models
class OrderItem(BaseModel):
    id: str
    name: str
    price: float
    quantity: int

class Order(BaseModel):
    items: List[OrderItem]
    total: float
    table_number: Optional[int] = None
    payment_method: str # 'online' or 'counter'

# Mock Data
MENU = [
    {"id": "b1", "name": "Classic Burger", "price": 12.99, "category": "Main", "image": "https://images.unsplash.com/photo-1568901346375-23c9450c58cd?auto=format&fit=crop&w=500&q=60"},
    {"id": "b2", "name": "Cheese Lava Burger", "price": 15.99, "category": "Main", "image": "https://images.unsplash.com/photo-1550547660-d9450f859349?auto=format&fit=crop&w=500&q=60"},
    {"id": "p1", "name": "Margherita Pizza", "price": 14.50, "category": "Main", "image": "https://images.unsplash.com/photo-1574071318508-1cdbab80d002?auto=format&fit=crop&w=500&q=60"},
    {"id": "d1", "name": "Coca Cola", "price": 2.50, "category": "Drink", "image": "https://images.unsplash.com/photo-1622483767028-3f66f32aef97?auto=format&fit=crop&w=500&q=60"},
    {"id": "d2", "name": "Lemonade", "price": 3.00, "category": "Drink", "image": "https://images.unsplash.com/photo-1513558161293-cdaf765ed2fd?auto=format&fit=crop&w=500&q=60"},
]

@app.get("/api/menu")
async def get_menu():
    return MENU

@app.post("/api/order")
async def create_order(order: Order):
    print(f"Received Order: {order}")
    
    # Simulate Processing
    time.sleep(1)
    
    # Simulate "Sending to Printer"
    print("--------------------------------")
    print("🖨️  KITCHEN PRINTER INTERFACE  🖨️")
    print(f"Table: {order.table_number}")
    for item in order.items:
        print(f" - {item.quantity}x {item.name}")
    print("--------------------------------")

    if order.payment_method == 'counter':
        print("Payment Pending: Customer will pay at counter.")
    else:
        print("Payment Processed: Online.")

    return {"status": "confirmed", "message": "Order received!"}

# Serve Static Files (Frontend)
app.mount("/", StaticFiles(directory="app/static", html=True), name="static")

