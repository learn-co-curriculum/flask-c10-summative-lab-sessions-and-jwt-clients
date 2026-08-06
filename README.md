# Productivity App - Flask Backend API

## Project Description

Productivity App is a secure Flask REST API backend that allows users to create and manage personal notes.

The API supports:

- User registration and login
- Secure password hashing using Flask-Bcrypt
- Session-based authentication
- User-owned notes
- Full CRUD operations for notes
- Pagination for notes listing
- Authorization so users can only access their own notes

Each user has their own private notes. Users cannot view, edit, or delete notes belonging to other users.

---

# Technologies Used

- Python 3.8+
- Flask
- Flask-SQLAlchemy
- Flask-Migrate
- Flask-Bcrypt
- Marshmallow
- SQLite
- Faker
- Git and GitHub

---

# Project Structure

```
productivity-app/
│
├── server/
│   ├── app.py              # Flask application setup
│   ├── config.py           # Application configuration
│   ├── models.py           # Database models
│   ├── schemas.py          # Marshmallow serialization
│   ├── decorators.py       # Authentication decorator
│   ├── seed.py             # Database seed data
│   │
│   └── routes/
│       ├── auth.py         # Authentication routes
│       └── notes.py        # Notes CRUD routes
│
├── migrations/             # Database migrations
├── Pipfile                 # Project dependencies
└── README.md
```

---

# Installation

## 1. Clone the repository

```bash
git clone <repository-url>
```

Move into the project:

```bash
cd productivity-app
```

---

## 2. Create virtual environment

Using Pipenv:

```bash
pipenv install
```

Activate environment:

```bash
pipenv shell
```

---

# Database Setup

Set Flask application:

```bash
export FLASK_APP=server.app
```

Initialize migrations:

```bash
flask db init
```

Create migration:

```bash
flask db migrate -m "Create users and notes tables"
```

Apply migration:

```bash
flask db upgrade
```

---

# Seed Database

Create sample users and notes:

```bash
python -m server.seed
```

The seed creates:

- 3 users
- Multiple notes for each user

Default password:

```
password123
```

---

# Running the Application

Start Flask server:

```bash
python -m server.app
```

The API runs on:

```
http://127.0.0.1:5555
```

---

# Authentication Endpoints

## Register User

### POST `/signup`

Creates a new user account.

Request:

```json
{
    "username": "rahab",
    "password": "password123"
}
```

Response:

```json
{
    "id": 1,
    "username": "rahab"
}
```

---

## Login User

### POST `/login`

Logs a user in and creates a session.

Request:

```json
{
    "username": "rahab",
    "password": "password123"
}
```

---

## Check Current Session

### GET `/check_session`

Returns the logged-in user.

Response:

```json
{
    "id": 1,
    "username": "rahab"
}
```

---

## Logout User

### DELETE `/logout`

Removes the user's session.

---

# Notes Endpoints

All note routes require authentication.

---

## Get Notes (Pagination)

### GET `/notes`

Returns notes belonging only to the logged-in user.

Example:

```
/notes?page=1&per_page=5
```

Response:

```json
{
    "notes": [],
    "total": 10,
    "pages": 2,
    "current_page": 1,
    "per_page": 5
}
```

---

## Get Single Note

### GET `/notes/<id>`

Example:

```
GET /notes/1
```

Returns a single note owned by the current user.

---

## Create Note

### POST `/notes`

Creates a new note.

Request:

```json
{
    "title": "Learning Flask",
    "content": "Building my first API",
    "category": "School"
}
```

---

## Update Note

### PATCH `/notes/<id>`

Updates an existing note.

Request:

```json
{
    "title": "Updated title"
}
```

---

## Delete Note

### DELETE `/notes/<id>`

Deletes a user's note.

---

# Security Features

## Password Protection

Passwords are never stored as plain text.

The application uses Flask-Bcrypt to:

- Hash passwords before saving
- Compare login passwords securely

---

## Authorization

Users can only access their own notes.

Example:

- User A creates Note 1
- User B cannot view Note 1
- User B cannot update or delete Note 1

---

# Testing

The API can be tested using:

- Postman
- Curl
- Frontend client application

Example signup test:

```bash
curl -X POST http://127.0.0.1:5555/signup \
-H "Content-Type: application/json" \
-d '{"username":"rahab","password":"password123"}'
```

---

# Git Development History

The project was built step-by-step:

```
Initial Flask project setup

Created User and Note models

Added Marshmallow schemas

Added authentication routes

Added notes CRUD routes

Created database migrations and seed data

Tested authentication and authorization
```

---

# Author

Rahab Wanja

Software Engineering Student

Moringa School