# Flask Authentication & Notes API
Description
This project is a Flask backend application that implements full authentication using JWT and a protected CRUD resource (Notes).
Users can register, log in, receive a JWT token, and manage their own notes securely.
All protected routes require authentication, and users can only access their own data.

## Technologies Used
	•	Python
	•	Flask
	•	Flask-JWT-Extended
	•	Flask-SQLAlchemy
	•	Flask-Migrate
	•	SQLite
	•	Pipenv

### Installation
1. Clone the repository:
``` bash 
git clone <your-repository-url>
cd flask-c10-summative-lab-sessions-and-jwt-clients
```
2. Install dependencies:
``` bash
pipenv install
```
3. Activate the virtual environment:
``` bash
pipenv shell
```
4. Run database migrations:
```bash
flask db upgrade
```
5. (Optional) Seed the database:
``` bash
python manage.py seed
```

### Running the Server
``` bash
flask run
```
The server will start at:
``` bash
http://127.0.0.1:5555
```

### Authentication Flow

Register
POST /signup
Body:
{
  "username": "testuser",
  "password": "password"
}

Login
POST /login

Response includes a JWT token:
{
  "token": "<JWT_TOKEN>",
  "user": {
    "id": 1,
    "username": "testuser"
  }
}

Check Current User
GET /me

Header:
Authorization: Bearer <JWT_TOKEN>

### Notes Resource (Protected)

All notes routes require:
Authorization: Bearer <JWT_TOKEN>

Create Note
POST /notes

Get Notes (with pagination)
GET /notes?page=1

Get Single Note
GET /notes/<id>

Update Note
PATCH /notes/<id>

Delete Note
DELETE /notes/<id>

Users can only access and modify their own notes.

## Features Summary
	•	JWT-based authentication
	•	Secure password hashing
	•	Protected routes
	•	User-specific resources
	•	Full CRUD functionality
	•	Pagination support
	•	Clean project structure

## Testing

All endpoints were tested using curl with valid and invalid JWT tokens to verify authentication, authorization, and error handling.
    


