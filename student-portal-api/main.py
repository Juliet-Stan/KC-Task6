from fastapi import FastAPI, HTTPException, Depends
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from pydantic import BaseModel
from typing import List, Dict
import json
import hashlib
import os

app = FastAPI()
security = HTTPBasic()

class Student(BaseModel):
    username: str
    password: str
    grades: Dict[str, float]

students = {}

def load_students():
    global students
    try:
        with open('students.json', 'r') as f:
            students = json.load(f)
    except FileNotFoundError:
        pass

def save_students():
    global students
    with open('students.json', 'w') as f:
        json.dump(students, f)

load_students()

@app.post("/register/")
def register(student: Student):
    if student.username in students:
        raise HTTPException(status_code=400, detail="Username already taken")
    students[student.username] = {
        "password": hashlib.sha256(student.password.encode()).hexdigest(),
        "grades": student.grades
    }
    save_students()
    return {"message": "Student registered successfully"}

@app.post("/login/")
def login(credentials: HTTPBasicCredentials = Depends(security)):
    if credentials.username not in students:
        raise HTTPException(status_code=401, detail="Invalid username or password")
    if hashlib.sha256(credentials.password.encode()).hexdigest() != students[credentials.username]["password"]:
        raise HTTPException(status_code=401, detail="Invalid username or password")
    return {"message": "Login successful"}

@app.get("/grades/")
def get_grades(credentials: HTTPBasicCredentials = Depends(security)):
    if credentials.username not in students:
        raise HTTPException(status_code=401, detail="Invalid username or password")
    return {"grades": students[credentials.username]["grades"]}
