
API Documentation: Notes API 📝
This API is a secure personal notes application built with FastAPI and JWT (JSON Web Tokens) for authentication. It allows users to register, log in, and manage their own private notes.

Features
User Authentication: Secure user registration with password hashing and JWT-based login.

Private Notes: Each user can only create, view, update, and delete their own notes.

Data Persistence: All user and note data is saved to local JSON files (users.json, notes.json) to ensure data is not lost between sessions.

CRUD Operations: Full functionality to Create, Read, Update, and Delete notes.

Requirements
You'll need Python 3.7 or higher and the following libraries:

Bash

pip install fastapi uvicorn python-multipart python-jose[cryptography] passlib
Note: python-jose and passlib are crucial for handling JWTs and password hashing.

Getting Started
Create your project files. Ensure you have the following two empty JSON files in the same directory as your main.py file:

users.json

notes.json

Run the application. From your terminal, execute the following command:

Bash

uvicorn main:app --reload
Access the documentation. View the interactive API documentation at http://127.0.0.1:8000/docs in your browser.

Testing with Postman 🧪
Postman is ideal for testing this API, as it simplifies the process of handling JWTs.

Step 1: Register a New User
Method: POST

URL: http://127.0.0.1:8000/register/

Body: Select raw and JSON.

JSON

{
  "username": "tester",
  "password": "password"
}
Send: You should receive a 200 OK response. Your users.json file will now contain the new user with a hashed password.

Step 2: Log In and Get a JWT
This is the most critical step. The server will generate a JWT for you.

Method: POST

URL: http://127.0.0.1:8000/login/

Body: Select raw and JSON.

JSON

{
  "username": "tester",
  "password": "password"
}
Send: You will get a 200 OK response with a long, encoded string called access_token. Copy this token.

Step 3: Add a New Note
You must use the JWT from the previous step to authenticate this request.

Method: POST

URL: http://127.0.0.1:8000/notes/

Authorization: Select Bearer Token.

Token: Paste the JWT you copied in the previous step.

Body: Select raw and JSON.

JSON

{
  "title": "My First Note",
  "content": "This is the content of my first note. It's about a dog."
}
Send: You will get a 200 OK response with a "Note added successfully" message.

Step 4: View Your Notes
This verifies that the note was saved correctly and that you can only see your own notes.

Method: GET

URL: http://127.0.0.1:8000/notes/

Authorization: Select Bearer Token.

Token: Use the same JWT as before.

Send: You will get a 200 OK response showing a list of your notes, including the one you just created.