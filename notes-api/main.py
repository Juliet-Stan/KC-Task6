
from fastapi import FastAPI, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel
from typing import List, Dict
import json
import jwt
import os
import hashlib
import uuid
from datetime import datetime, timedelta

app = FastAPI()

# A strong, securely stored secret key. Use an environment variable in production.
JWT_SECRET_KEY = os.environ.get("JWT_SECRET_KEY", "b421a7d6e4c8f5b3a9d2c6e1f0a8c4b2a6f8e7d9c0b1f2e3d4c5a6b7d8e9f0a1")
ALGORITHM = "HS256"

# OAuth2PasswordBearer dependency for handling the token
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# --- Pydantic Models ---
class UserIn(BaseModel):
    username: str
    password: str

class NoteIn(BaseModel):
    title: str
    content: str

class NoteOut(BaseModel):
    id: str
    title: str
    content: str
    date: str

# --- In-Memory Databases ---
users = {}
notes = {}

# --- File I/O Functions ---
def load_users():
    global users
    try:
        with open('users.json', 'r') as f:
            users.update(json.load(f))
    except (FileNotFoundError, json.JSONDecodeError):
        pass

def save_users():
    global users
    with open('users.json', 'w') as f:
        json.dump(users, f, indent=2)

def load_notes():
    global notes
    try:
        with open('notes.json', 'r') as f:
            notes.update(json.load(f))
    except (FileNotFoundError, json.JSONDecodeError):
        pass

def save_notes():
    global notes
    with open('notes.json', 'w') as f:
        json.dump(notes, f, indent=2)

load_users()
load_notes()

# --- Authentication & Authorization Logic ---
def get_hashed_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()

def authenticate_user(username: str, password: str = None):
    if username not in users:
        raise HTTPException(status_code=401, detail="User not found")
    user_data = users[username]
    if password and user_data.get("password") != get_hashed_password(password):
        raise HTTPException(status_code=401, detail="Invalid password")
    return user_data

def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, JWT_SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def get_current_user_from_token(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=401, detail="Invalid token payload")
        authenticate_user(username)
        return username
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")

# --- Endpoints ---
@app.post("/register/")
def register(user: UserIn):
    if user.username in users:
        raise HTTPException(status_code=400, detail="Username already exists")
    users[user.username] = {"password": get_hashed_password(user.password)}
    save_users()
    return {"message": "User registered successfully"}

@app.post("/login/")
def login(user_data: UserIn):
    authenticate_user(user_data.username, user_data.password)
    access_token = create_access_token(
        data={"sub": user_data.username}
    )
    return {"access_token": access_token, "token_type": "bearer"}

@app.post("/notes/")
def add_note(note: NoteIn, username: str = Depends(get_current_user_from_token)):
    if username not in notes:
        notes[username] = []
    
    note_id = str(uuid.uuid4())
    new_note = {
        "id": note_id,
        "title": note.title,
        "content": note.content,
        "date": datetime.utcnow().isoformat()
    }
    notes[username].append(new_note)
    save_notes()
    return {"message": "Note added successfully", "note_id": note_id}

@app.get("/notes/")
def get_notes(username: str = Depends(get_current_user_from_token)):
    return notes.get(username, [])

@app.get("/notes/{note_id}")
def get_note(note_id: str, username: str = Depends(get_current_user_from_token)):
    user_notes = notes.get(username, [])
    for note in user_notes:
        if note["id"] == note_id:
            return note
    raise HTTPException(status_code=404, detail="Note not found")

@app.put("/notes/{note_id}")
def update_note(note_id: str, updated_note: NoteIn, username: str = Depends(get_current_user_from_token)):
    user_notes = notes.get(username, [])
    for i, note in enumerate(user_notes):
        if note["id"] == note_id:
            user_notes[i]["title"] = updated_note.title
            user_notes[i]["content"] = updated_note.content
            user_notes[i]["date"] = datetime.utcnow().isoformat()
            save_notes()
            return {"message": "Note updated successfully"}
    raise HTTPException(status_code=404, detail="Note not found")

@app.delete("/notes/{note_id}")
def delete_note(note_id: str, username: str = Depends(get_current_user_from_token)):
    user_notes = notes.get(username, [])
    for i, note in enumerate(user_notes):
        if note["id"] == note_id:
            del user_notes[i]
            save_notes()
            return {"message": "Note deleted successfully"}
    raise HTTPException(status_code=404, detail="Note not found")