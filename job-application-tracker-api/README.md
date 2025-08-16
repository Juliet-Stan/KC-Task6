
Job Application Tracker API 🚀
This is a secure API designed to help users track their job applications. Each user can register an account, log in, and manage only their own applications. The API also tracks the number of applicants for pre-defined job listings.

Features
User Authentication: Secure user registration and login with hashed passwords.

Per-User Data: Each user's job applications are stored separately, ensuring they can only access their own data.

Job Listings: The API references a set of predefined job listings, allowing users to apply with a simple ID. The number of applicants for each listing is also tracked.

Data Persistence: All user and application data is saved to local JSON files (users.json, applications.json, and job_listings.json), ensuring data is not lost when the server restarts.

Requirements
You'll need Python 3.7 or higher. Install the required libraries using pip:

Bash

pip install fastapi uvicorn python-multipart
Getting Started
Create your project files. Make sure the following three empty JSON files are in the same directory as your main.py file:

users.json

applications.json

job_listings.json

Add a job listing. Open job_listings.json and paste the following content inside. This is crucial for the API to work.

JSON

{
  "1": {
    "title": "Senior Software Engineer",
    "company": "Tech Innovations Inc.",
    "description": "Develop and maintain our core platform.",
    "applicants": 0
  },
  "2": {
    "title": "Data Scientist",
    "company": "Data Insights Co.",
    "description": "Analyze complex data sets to derive business insights.",
    "applicants": 0
  }
}
Run the application. From your terminal, execute the following command to start the server:

Bash

uvicorn main:app --reload
Access the documentation. You can view and interact with the API's endpoints at http://127.0.0.1:8000/docs.

Testing with Postman 🧪
Postman is the best way to test this API's authentication flow. Follow these steps in order.

Step 1: Register a New User
Method: POST

URL: http://127.0.0.1:8000/register/

Body: Select raw and JSON from the dropdown.

JSON

{
  "username": "tester",
  "password": "password",
  "role": "customer"
}
Send: You should receive a 200 OK response.

Step 2: Log In to Get a Bearer Token
This step logs you in and returns a token needed for authenticated endpoints.

Method: POST

URL: http://127.0.0.1:8000/login/

Authorization: Select Basic Auth.

Username: tester

Password: password

Send: The response will be 200 OK with a token. The token value is the username (tester). Copy this value.

Step 3: View Available Job Listings
This endpoint is public, so no authentication is needed.

Method: GET

URL: http://127.0.0.1:8000/job_listings/

Send: The response will be 200 OK and show the list of available jobs.

Step 4: Add a Job Application
Now you will use your token to apply for a job.

Method: POST

URL: http://127.0.0.1:8000/applications/?job_listing_id=1

Authorization: Select Bearer Token.

Token: Paste the token (tester) you copied in Step 2.

Send: The response will be 200 OK with a success message.

Step 5: View Your Applications
Method: GET

URL: http://127.0.0.1:8000/applications/

Authorization: Select Bearer Token.

Token: Use the same token from Step 4.

Send: The response will be 200 OK and show your application(s).