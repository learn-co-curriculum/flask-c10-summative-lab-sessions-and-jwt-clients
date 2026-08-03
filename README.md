# Productivity Task Tracker API

## Overview

The Productivity Task Tracker API is a secure Flask backend application that allows users to create and manage personal tasks. Each user has their own account and can securely create, view, update, and delete only their own tasks.

The application uses **session-based authentication**, **Flask-SQLAlchemy**, **Flask-Migrate**, and **Flask-Bcrypt** to provide secure authentication and data protection.

---

## Features

* User registration
* Secure password hashing with Bcrypt
* User login and logout using Flask sessions
* Persistent login with session checking
* User-owned task management
* Full CRUD operations
* Protected routes
* Pagination for task listings
* Database seeding
* Automated testing with Pytest

---

## Technologies Used

* Python 3
* Flask
* Flask-RESTful
* Flask-SQLAlchemy
* Flask-Migrate
* Flask-Bcrypt
* Marshmallow
* SQLite
* Pytest

---

# Installation

Clone the repository:

```bash
git clone https://github.com/Christin115/flask-c10-summative-lab-sessions-and-jwt-clients.git
```

Navigate into the project:

```bash
cd flask-c10-summative-lab-sessions-and-jwt-clients
```

Create a virtual environment:

```bash
python3 -m venv .venv
```

Activate the virtual environment:

Linux / macOS

```bash
source .venv/bin/activate
```

Windows

```powershell
.venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

---

# Database Setup

Run the migrations:

```bash
flask --app server.app db upgrade
```

Seed the database:

```bash
python -m server.seed
```

Demo users are automatically created.

Demo password:

```text
password123
```

---

# Running the Application

Start the backend:

```bash
flask --app server.app run --port 5555
```

The API will be available at:

```
http://127.0.0.1:5555
```

---

# Running Tests

Execute all tests:

```bash
pytest -v
```

---

# API Endpoints

## Authentication

### POST /signup

Creates a new user account.

Example Request

```json
{
  "username": "christin115",
  "password": "password123",
  "password_confirmation": "password123"
}
```

---

### POST /login

Logs an existing user into the application.

---

### GET /check_session

Returns the currently logged-in user.

---

### DELETE /logout

Logs the current user out.

---

# Tasks

All task routes require authentication.

---

## GET /tasks

Returns the authenticated user's tasks.

Supports pagination.

Example:

```
GET /tasks?page=1&per_page=5
```

---

## POST /tasks

Creates a new task.

Example

```json
{
  "title": "Complete Flask Project",
  "description": "Finish backend API",
  "completed": false
}
```

---

## GET /tasks/<id>

Returns a single task belonging to the logged-in user.

---

## PATCH /tasks/<id>

Updates an existing task.

Example

```json
{
  "completed": true
}
```

---

## DELETE /tasks/<id>

Deletes a task owned by the authenticated user.

---

# Authentication

This project uses **Flask Sessions** for authentication.

Passwords are never stored as plain text.

Passwords are securely hashed using Flask-Bcrypt before being saved in the database.

Only authenticated users can access protected routes.

Users can only access their own tasks.

---

# Pagination

Task listings support pagination.

Example:

```
GET /tasks?page=2&per_page=5
```

Response includes:

* current page
* items per page
* total items
* total pages
* next page indicator
* previous page indicator

---

# Project Structure

```
flask-c10-summative-lab-sessions-and-jwt-clients/

│
├── client-with-jwt/
├── client-with-sessions/
├── migrations/
├── server/
│   ├── app.py
│   ├── models.py
│   ├── schemas.py
│   └── seed.py
│
├── tests/
│   ├── conftest.py
│   ├── test_auth.py
│   └── test_tasks.py
│
├── requirements.txt
├── pytest.ini
├── .env.example
├── .gitignore
└── README.md
```

---

# Security

* Passwords are hashed with Bcrypt.
* Authentication is handled using Flask sessions.
* Unauthorized users receive a **401 Unauthorized** response.
* Users cannot create, edit, view, or delete another user's tasks.

---

# Future Improvements

* Task due dates
* Task priorities
* Categories
* Search functionality
* Sorting
* Task reminders
* Frontend deployment

---


