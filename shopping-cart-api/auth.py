
from fastapi import HTTPException
from pydantic import BaseModel
import json
import hashlib
import os

class User(BaseModel):
    username: str
    password: str
    role: str

def get_hashed_password(password: str) -> str:
    """Hashes the password using SHA-256."""
    return hashlib.sha256(password.encode()).hexdigest()

def load_users():
    """Loads users from the users.json file."""
    try:
        with open('users.json', 'r') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        # Return an empty dictionary if the file doesn't exist or is empty
        return {}

def save_users(users: dict):
    """Saves users to the users.json file."""
    with open('users.json', 'w') as f:
        json.dump(users, f, indent=2)

def authenticate_user(username: str, password: str = None):
    """Authenticates a user by checking their username and password."""
    users = load_users()
    if username not in users:
        raise HTTPException(status_code=401, detail="User not found")

    user_data = users[username]
    if password:
        if user_data.get("password") != get_hashed_password(password):
            raise HTTPException(status_code=401, detail="Invalid password")

    return user_data

def get_user_role(username: str):
    """Retrieves the role of a user."""
    users = load_users()
    if username not in users:
        raise HTTPException(status_code=401, detail="User not found")
    return users[username]["role"]

def register_user(username: str, password: str, role: str):
    """Registers a new user with a hashed password."""
    users = load_users()
    if username in users:
        raise HTTPException(status_code=400, detail="Username already exists")

    users[username] = {
        "password": get_hashed_password(password),
        "role": role
    }
    save_users(users)