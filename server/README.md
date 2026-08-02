# Task Tracker API

## Project Description

Task Tracker API is a secure RESTful Flask backend that allows users to register, log in, and manage their personal tasks. Authentication is implemented using JSON Web Tokens (JWT), ensuring that only authenticated users can access protected endpoints. Each user can only create, view, update, and delete their own tasks.

This project was developed as part of the Flask Authentication Summative Lab.

---

## Features

- User Registration
- User Login with JWT Authentication
- Password Hashing using Flask-Bcrypt
- Protected Routes using JWT
- User-specific Task Management
- Full CRUD Operations
- Pagination for Task Listing
- Database Migrations with Flask-Migrate
- Database Seeding

---

## Technologies Used

- Python 3.8+
- Flask
- Flask-RESTful
- Flask-SQLAlchemy
- Flask-Migrate
- Flask-Bcrypt
- Flask-JWT-Extended
- SQLite
- Marshmallow
- Postman

---

## Project Structure

```
server/
│
├── app.py
├── config.py
├── models.py
├── seed.py
├── Pipfile
├── README.md
│
├── resources/
│   ├── auth.py
│   └── task.py
│
├── migrations/
│
└── instance/
    └── app.db
```

---

## Installation

### 1. Clone the repository

```bash
git clone <repository-url>
```

### 2. Navigate into the server directory

```bash
cd server
```

### 3. Install dependencies

```bash
pipenv install
```

### 4. Activate the virtual environment

```bash
pipenv shell
```

---

## Environment Setup

Set the Flask application:

```bash
export FLASK_APP=app.py
```

---

## Database Setup

Initialize migrations (only once):

```bash
flask db init
```

Create migration:

```bash
flask db migrate -m "Initial migration"
```

Apply migrations:

```bash
flask db upgrade
```

---

## Seed the Database

Run:

```bash
python seed.py
```

This creates sample users and tasks.

---

## Running the Application

```bash
flask run
```

The API runs at:

```
http://127.0.0.1:5000
```

---

# Authentication

JWT Authentication is used.

Protected routes require the Authorization header:

```
Authorization: Bearer <JWT_TOKEN>
```

Obtain the token by logging in through the `/login` endpoint.

---

# API Endpoints

## Authentication

### Register User

```
POST /signup
```

Example Request

```json
{
    "username": "emmanuel",
    "email": "emmanuel@gmail.com",
    "password": "123456"
}
```

---

### Login

```
POST /login
```

Example Request

```json
{
    "email": "emmanuel@gmail.com",
    "password": "123456"
}
```

Returns a JWT access token.

---

### Current User

```
GET /me
```

Protected Route

Returns the currently authenticated user.

---

# Task Endpoints

## Get All Tasks

```
GET /tasks
```

Protected

Supports pagination.

Example:

```
/tasks?page=1&per_page=5
```

---

## Create Task

```
POST /tasks
```

Example

```json
{
    "title": "Complete Flask Lab",
    "description": "Finish CRUD implementation"
}
```

---

## Get One Task

```
GET /tasks/<id>
```

Protected

---

## Update Task

```
PATCH /tasks/<id>
```

Example

```json
{
    "status": "Completed"
}
```

---

## Delete Task

```
DELETE /tasks/<id>
```

Protected

---

# Security Features

- Passwords are hashed using Flask-Bcrypt.
- JWT authentication protects sensitive endpoints.
- Users can only access their own tasks.
- Unauthorized requests return appropriate HTTP status codes.

---

# Pagination

Task listing supports pagination.

Example:

```
GET /tasks?page=2&per_page=5
```

Response includes:

- current page
- total pages
- total records

---

# Testing

The API was tested using Postman.

Tested endpoints include:

- User Registration
- Login
- Current User
- Create Task
- Get Tasks
- Get Task by ID
- Update Task
- Delete Task

---

# Author

**Emmanuel Sum Kipkorir**

GitHub:
https://github.com/Kip-sum

---

# License

This project was created for educational purposes as part of the Flask Authentication Summative Lab.