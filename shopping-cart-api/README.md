
Shopping Cart API
This project is a secure shopping cart API built with FastAPI. It features a role-based access control system where only authenticated administrators can add products, while all registered users can browse products, manage a shopping cart, and check out.

Features
User Management: Register and authenticate users with hashed passwords.

Role-Based Access:

POST /admin/add_product/: Restricted to users with the admin role.

POST /cart/add/ and POST /cart/checkout/: Restricted to authenticated users.

GET /products/: Publicly accessible.

Data Persistence: All user, product, and cart data is saved to local JSON files (users.json, products.json, and cart.json).

Requirements
Python 3.7+

fastapi

uvicorn

python-multipart (if you plan to handle file uploads)

You can install the necessary packages using pip:

Bash

pip install fastapi uvicorn python-multipart
Getting Started
Clone the repository or create your project files.

Create your project files:

main.py

auth.py

users.json (Start with {} inside)

products.json (Start with {} inside)

cart.json (Start with {} inside)

Copy the code for main.py and auth.py into their respective files.

Run the application from your terminal:

Bash

uvicorn main:app --reload
Access the interactive API documentation by visiting http://127.0.0.1:8000/docs in your browser.

API Endpoints
Endpoint	Method	Authentication	Description
/register/	POST	None	Creates a new user.
/login/	POST	Basic Auth	Authenticates a user and returns a token.
/admin/add_product/	POST	Basic Auth (Admin)	Adds a new product to the inventory.
/products/	GET	None	Lists all available products.
/cart/add/	POST	Bearer Token	Adds a product to the user's cart.
/cart/checkout/	POST	Bearer Token	Checks out the user's cart and returns the total price.
Testing with Postman
Postman is recommended for testing this API as it provides excellent control over authentication headers.

Step 1: Register a New User
Since the API starts with no users, you must register a new account first.

Method: POST

URL: http://127.0.0.1:8000/register/

Body: Select raw and JSON.

JSON

{
  "username": "customer1",
  "password": "password1",
  "role": "customer"
}
Send: You should see a 200 OK response.

Step 2: Register an Admin User
To test the admin endpoint, you must create an admin account.

Method: POST

URL: http://127.0.0.1:8000/register/

Body: Select raw and JSON.

JSON

{
  "username": "admin",
  "password": "admin",
  "role": "admin"
}
Send: You should see a 200 OK response.

Step 3: Add a Product (as Admin)
Use the admin credentials to add a product.

Method: POST

URL: http://127.0.0.1:8000/admin/add_product/

Authorization: Select Basic Auth.

Username: admin

Password: admin

Body: Select raw and JSON.

JSON

{
  "id": 1,
  "name": "Laptop",
  "price": 1200.00
}
Send: You should see a 200 OK response.

Step 4: Get a Bearer Token (as a Customer)
You need to log in as a regular customer to get a token for the cart endpoints.

Method: POST

URL: http://127.0.0.1:8000/login/

Authorization: Select Basic Auth.

Username: customer1

Password: password1

Send: You should receive a 200 OK response with a token. Copy this token value (customer1).

Step 5: Add to Cart (as a Customer)
Use the token you just received to add a product to your cart.

Method: POST

URL: http://127.0.0.1:8000/cart/add/?product_id=1

Authorization: Select Bearer Token.

Token: Paste the token (customer1) you copied.

Send: You should see a 200 OK response.

Step 6: Checkout (as a Customer)
Use your token to check out your cart.

Method: POST

URL: http://127.0.0.1:8000/cart/checkout/

Authorization: Select Bearer Token.

Token: Ensure your token (customer1) is still in the field.

Send: You should see a 200 OK response with the total_price.