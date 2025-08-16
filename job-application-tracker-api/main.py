
from fastapi import FastAPI, HTTPException, Depends, Header
from fastapi.security import HTTPBearer, HTTPBasic
from fastapi.security.http import HTTPBasicCredentials, HTTPAuthorizationCredentials
from pydantic import BaseModel
from typing import List, Dict
import json
import hashlib
import base64
import os
import datetime 

# --- App Initialization ---
app = FastAPI()
security = HTTPBearer()
basic_security = HTTPBasic()

# --- In-Memory Databases ---
users = {}
applications = {}
job_listings = {}

# --- Pydantic Models ---
# This model is no longer used for the request body
class JobApplication(BaseModel):
    job_listing_id: str
    date_applied: str
    status: str

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

def load_applications():
    global applications
    try:
        with open('applications.json', 'r') as f:
            applications.update(json.load(f))
    except (FileNotFoundError, json.JSONDecodeError):
        pass

def save_applications():
    global applications
    with open('applications.json', 'w') as f:
        json.dump(applications, f, indent=2)

def load_job_listings():
    global job_listings
    try:
        with open('job_listings.json', 'r') as f:
            job_listings.update(json.load(f))
    except (FileNotFoundError, json.JSONDecodeError):
        pass

def save_job_listings():
    global job_listings
    with open('job_listings.json', 'w') as f:
        json.dump(job_listings, f, indent=2)

# Load data on startup
load_users()
load_applications()
load_job_listings()

# --- Authentication & Authorization Logic ---
def get_hashed_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()

def authenticate_user(username: str, password: str = None):
    if username not in users:
        raise HTTPException(status_code=401, detail="User not found")
    user_data = users[username]
    if password:
        if user_data.get("password") != get_hashed_password(password):
            raise HTTPException(status_code=401, detail="Invalid password")
    return user_data

def get_current_user_token(token: HTTPAuthorizationCredentials = Depends(security)):
    try:
        authenticate_user(token.credentials)
    except HTTPException as e:
        raise e
    return token.credentials

# --- Endpoints ---
@app.post("/register/")
def register(username: str, password: str):
    if username in users:
        raise HTTPException(status_code=400, detail="Username already exists")
    users[username] = {"password": get_hashed_password(password)}
    save_users()
    return {"message": "User registered successfully"}

@app.post("/login/")
def login(credentials: HTTPBasicCredentials = Depends(basic_security)):
    authenticate_user(credentials.username, credentials.password)
    return {"message": "Login successful", "token": credentials.username}

@app.get("/job_listings/")
def get_job_listings():
    return job_listings

# Corrected Endpoint
@app.post("/applications/")
def add_application(job_listing_id: str, username: str = Depends(get_current_user_token)):
    if job_listing_id not in job_listings:
        raise HTTPException(status_code=404, detail="Job listing not found")

    if username not in applications:
        applications[username] = []
    
    application_details = {
        "job_title": job_listings[job_listing_id]["title"],
        "company": job_listings[job_listing_id]["company"],
        "date_applied": datetime.date.today().isoformat(), # Automatically set the current date
        "status": "pending" # Default status
    }
    applications[username].append(application_details)
    save_applications()

    # Increment applicant count and save to file
    job_listings[job_listing_id]["applicants"] += 1
    save_job_listings()

    return {"message": "Application added successfully"}

@app.get("/applications/")
def get_applications(username: str = Depends(get_current_user_token)):
    if username not in applications:
        return []
    return applications[username]