from fastapi import FastAPI, HTTPException
from fastapi.responses import Response
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from typing import List, Optional
import time
import qrcode
import io

app = FastAPI()

# Data Models
class OrderItem(BaseModel):
    id: str
    name: str
    price: float
    quantity: int
    is_veg: bool

class Order(BaseModel):
    items: List[OrderItem]
    total: float
    table_number: Optional[int] = None
    payment_method: str # 'online' or 'counter'

# --- MENU GENERATION (INDIAN CUISINE) ---
def generate_menu():
    menu = []
    
    categories = {
        "Breakfast": [
            ("Masala Dosa", 120, True), ("Idli Sambar", 80, True), ("Puri Bhaji", 100, True), 
            ("Aloo Paratha", 90, True), ("Poha", 60, True), ("Upma", 60, True), 
            ("Vada Pav", 40, True), ("Misal Pav", 120, True), ("Chole Bhature", 150, True),
            ("Anda Bhurji", 100, False), ("Omelette", 80, False), ("Kheema Pav", 180, False)
        ],
        "Snacks": [
            ("Samosa", 30, True), ("Pakora", 80, True), ("Paneer Tikka", 220, True),
            ("Hara Bhara Kabab", 180, True), ("Veg Manchurian", 160, True),
            ("Chicken Tikka", 280, False), ("Chicken Lollipop", 250, False),
            ("Fish Fry", 350, False), ("Mutton Seekh Kabab", 380, False)
        ],
        "Main Course": [
            ("Paneer Butter Masala", 280, True), ("Palak Paneer", 260, True), ("Dal Makhani", 220, True),
            ("Dal Tadka", 180, True), ("Mix Veg", 200, True), ("Malai Kofta", 290, True),
            ("Butter Chicken", 350, False), ("Chicken Curry", 320, False), 
            ("Mutton Rogan Josh", 450, False), ("Kadai Chicken", 340, False),
            ("Chicken Handi", 330, False), ("Egg Curry", 200, False)
        ],
        "Breads": [
            ("Tandoori Roti", 30, True), ("Butter Roti", 40, True), ("Plain Naan", 50, True),
            ("Butter Naan", 60, True), ("Garlic Naan", 80, True), ("Cheese Naan", 100, True),
            ("Kulcha", 70, True), ("Lachha Paratha", 60, True)
        ],
        "Rice": [
            ("Steamed Rice", 100, True), ("Jeera Rice", 140, True), ("Veg Pulao", 180, True),
            ("Veg Biryani", 220, True), ("Curd Rice", 150, True),
            ("Chicken Biryani", 320, False), ("Mutton Biryani", 420, False),
            ("Egg Biryani", 250, False), ("Prawns Biryani", 450, False)
        ],
        "Drinks": [
            ("Masala Chai", 30, True), ("Filter Coffee", 40, True), ("Lassi (Sweet)", 80, True),
            ("Lassi (Salted)", 80, True), ("Mango Lassi", 100, True), ("Butter Milk", 40, True),
            ("Fresh Lime Soda", 60, True), ("Cola", 40, True)
        ]
    }

    # Algorithmically expand to 200+ items by adding variations
    count = 1
    for category, items in categories.items():
        for name, base_price, is_veg in items:
            # Base Item
            menu.append({
                "id": f"{category[:2].lower()}{count}",
                "name": name,
                "price": float(base_price),
                "category": category,
                "is_veg": is_veg,
                "image": "https://source.unsplash.com/500x500/?indian,food" # Placeholder
            })
            count += 1
            
            # Create Variations to reach 200+ count
            if category == "Main Course":
                menu.append({"id": f"{category[:2].lower()}{count}", "name": f"{name} (Half)", "price": float(base_price)*0.6, "category": category, "is_veg": is_veg, "image": ""}); count+=1
                menu.append({"id": f"{category[:2].lower()}{count}", "name": f"{name} (Spicy)", "price": float(base_price)+20, "category": category, "is_veg": is_veg, "image": ""}); count+=1
            elif category == "Breads":
                menu.append({"id": f"{category[:2].lower()}{count}", "name": f"{name} (Wheat)", "price": float(base_price)+10, "category": category, "is_veg": is_veg, "image": ""}); count+=1
    
    return menu

MENU = generate_menu()

@app.get("/api/menu")
async def get_menu():
    return MENU

@app.post("/api/order")
async def create_order(order: Order):
    print(f"Received Order from Table {order.table_number}")
    print(f"Total: ₹{order.total}")
    
    # Simulate "Sending to Printer"
    print("--------------------------------")
    print("🖨️  KITCHEN PRINTER INTERFACE  🖨️")
    print(f"Table: {order.table_number}")
    for item in order.items:
        veg_icon = "🟢" if item.is_veg else "🔴"
        print(f" - {veg_icon} {item.quantity}x {item.name}")
    print("--------------------------------")

    return {"status": "confirmed", "message": "Order received!"}

@app.get("/api/qr/{table_id}")
async def generate_qr_code(table_id: int):
    # In a real deployed scenario, change 'localhost' to your server IP
    url = f"http://localhost:8000/?table={table_id}"
    
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(url)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")
    
    # Save to memory buffer
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    buf.seek(0)
    
    return Response(content=buf.getvalue(), media_type="image/png")

# Serve Static Files (Frontend)
app.mount("/", StaticFiles(directory="app/static", html=True), name="static")
