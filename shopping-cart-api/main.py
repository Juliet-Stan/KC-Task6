
from fastapi import FastAPI, HTTPException, Depends, Header
from fastapi.security import HTTPBearer, HTTPBasic
from fastapi.security.http import HTTPBasicCredentials, HTTPAuthorizationCredentials
from pydantic import BaseModel
from typing import List
import json
import hashlib
import os
import base64

app = FastAPI()
security = HTTPBearer()
admin_security = HTTPBasic()

class User(BaseModel):
    username: str
    password: str
    role: str

class Product(BaseModel):
    id: int
    name: str
    price: float

products = {}
cart = {}

def load_products():
    global products
    try:
        with open('products.json', 'r') as f:
            products = json.load(f)
    except FileNotFoundError:
        pass

def save_products():
    global products
    with open('products.json', 'w') as f:
        json.dump(products, f)

def load_cart():
    global cart
    try:
        with open('cart.json', 'r') as f:
            cart = json.load(f)
    except FileNotFoundError:
        pass

def save_cart():
    global cart
    with open('cart.json', 'w') as f:
        json.dump(cart, f)

load_products()
load_cart()

# Auth module
from auth import authenticate_user, get_user_role, get_hashed_password, register_user

@app.post("/register/")
def register(user: User):
    register_user(user.username, user.password, user.role)
    return {"message": "User registered successfully"}

@app.post("/login/")
def login(authorization: str = Header(None)):
    if not authorization or not authorization.startswith("Basic "):
        raise HTTPException(status_code=401, detail="Invalid authorization header. Use 'Basic username:password'")

    encoded_credentials = authorization.split(" ")[1]
    decoded_credentials = base64.b64decode(encoded_credentials).decode("utf-8")
    username, password = decoded_credentials.split(":", 1)

    user_data = authenticate_user(username, password)
    if not user_data:
        raise HTTPException(status_code=401, detail="Invalid username or password")

    return {"message": "Login successful", "token": username}

@app.post("/admin/add_product/")
def add_product(product: Product, credentials: HTTPBasicCredentials = Depends(admin_security)):
    username = credentials.username
    user_role = get_user_role(username)
    if user_role != "admin":
        raise HTTPException(status_code=403, detail="Only admins can add products")
    products[str(product.id)] = {
        "name": product.name,
        "price": product.price
    }
    save_products()
    return {"message": "Product added successfully"}

@app.get("/products/")
def get_products():
    products_with_ids = []
    for product_id, product_data in products.items():
        product_item = product_data.copy()
        product_item["id"] = product_id
        products_with_ids.append(product_item)
    return products_with_ids

@app.post("/cart/add/")
def add_to_cart(product_id: int, token: HTTPAuthorizationCredentials = Depends(security)):
    """
    Allows an authenticated user to add a product to their cart.
    """
    # The actual token string is in the .credentials attribute
    username = token.credentials
    authenticate_user(username)  # Checks if the user exists
    
    if str(product_id) not in products:
        raise HTTPException(status_code=404, detail="Product not found")
    
    if username not in cart:
        cart[username] = []
    cart[username].append(product_id)
    return {"message": "Product added to cart"}

@app.post("/cart/checkout/")
def checkout_cart(token: HTTPAuthorizationCredentials = Depends(security)):
    """
    Allows an authenticated user to checkout and clear their cart.
    """
    # The actual token string is in the .credentials attribute
    username = token.credentials
    authenticate_user(username)  # Checks if the user exists
    
    if username not in cart or not cart[username]:
        raise HTTPException(status_code=400, detail="Cart is empty")
    
    total_price = sum(products[str(product_id)]["price"] for product_id in cart[username] if str(product_id) in products)
    
    # Clear the cart after checkout
    cart[username] = []
    
    return {"message": "Checkout successful", "total_price": total_price}