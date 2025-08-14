Secure Student Portal API

Overview
This API provides a secure student portal where students can log in to view their grades. The API uses HTTP Basic authentication to authenticate students and authorize access to their grades.

Features
- Student registration with username and password
- Student login with HTTP Basic authentication
- Secure access to student grades
- Grades stored in a JSON file

Endpoints
POST /register/
- Register a new student with username and password
- Request Body: Student object with username and password fields
- Response: Success message with HTTP 201 status code

POST /login/
- Log in an existing student with username and password
- Request Headers: Authorization header with HTTP Basic credentials
- Response: Success message with HTTP 200 status code

GET /grades/
- Get the grades of the logged-in student
- Request Headers: Authorization header with HTTP Basic credentials
- Response: grades object with HTTP 200 status code

Requirements
- Python 3.9+
- FastAPI
- Uvicorn

Installation
1. Clone the repository: git clone https://github.com/your-username/secure-student-portal-api.git
2. Install the dependencies: pip install fastapi uvicorn
3. Run the API: uvicorn main:app --reload

Testing
Use a tool like Postman or cURL to test the API endpoints.

Contributing
Contributions are welcome! Please fork the repository, make your changes, and submit a pull request.

License
This project is licensed under the MIT License. See the LICENSE file for details.