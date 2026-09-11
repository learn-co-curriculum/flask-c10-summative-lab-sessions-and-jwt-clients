# Task Tracker API

A secure Flask REST API backend for a personal task-tracking productivity app. Users can register, log in, and manage their own private tasks — with authentication ensuring nobody can view or modify another user's data.

## Project Description

This API supports full user authentication (JWT-based, with session fallback) and complete CRUD functionality for a Task resource owned by each user. Every task-related endpoint is protected, ensuring users can only access their own tasks. The API also includes pagination on the tasks list endpoint.

Core features:
- User registration and login with hashed passwords (Flask-Bcrypt)
- JWT authentication for protected routes
- Full CRUD for tasks (Create, Read, Update, Delete)
- Ownership checks - users cannot access another user's tasks
- Paginated task listing
- Marshmallow schemas for serialization/validation

## Installation

1. Clone the repository:
   git clone https://github.com/mpaera/flask-c10-summative-lab-sessions-and-jwt-clients.git
   cd flask-c10-summative-lab-sessions-and-jwt-clients

2. Create and activate a virtual environment:
   python -m venv venv
   source venv/Scripts/activate

3. Install dependencies:
   pip install -r requirements.txt

4. Set up environment variables (optional, defaults exist for local dev). Create a .env file:
   SECRET_KEY=your-secret-key
   JWT_SECRET_KEY=your-jwt-secret-key
   DATABASE_URL=sqlite:///instance/app.db

5. Run database migrations:
   flask --app server.app db upgrade

6. Seed the database with demo data:
   python -m server.seed
   This creates a demo user (demo / demo123) with a sample task.

## Running the Application

Start the Flask development server:
   flask --app server.app run

The API will be available at http://127.0.0.1:5000.

## API Endpoints

### Authentication

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | /signup | Register a new user. Requires username, password, password_confirmation, optional email. Returns the user and a JWT token. |
| POST | /login | Log in with username and password. Returns the user and a JWT token. |
| GET | /me | Get the currently authenticated user (requires JWT bearer token). |
| GET | /check_session | Check if a session-based user is logged in. |
| DELETE | /logout | Log out the current session. |

### Tasks

All task endpoints require authentication (JWT bearer token or an active session) and only return/affect the logged-in user's own tasks.

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | /tasks?page=1&per_page=10 | Get a paginated list of the logged-in user's tasks. |
| POST | /tasks | Create a new task. Requires title; optional description, completed. |
| GET | /tasks/<id> | Get a single task by ID (must belong to the logged-in user). |
| PATCH | /tasks/<id> | Update a task (partial updates supported). |
| DELETE | /tasks/<id> | Delete a task. |

Pagination response shape (GET /tasks):

{
  "tasks": [...],
  "page": 1,
  "per_page": 10,
  "pages": 3,
  "total": 25,
  "has_next": true,
  "has_prev": false
}

## Tech Stack

- Flask
- Flask-SQLAlchemy
- Flask-Migrate
- Flask-JWT-Extended
- Flask-Bcrypt
- Marshmallow / Flask-Marshmallow / Marshmallow-SQLAlchemy

## Project Structure

server/
- app.py           Flask app factory, extension setup, blueprint registration
- config.py        App configuration (DB URI, secret keys)
- seed.py          Demo data seeding script
- models/          SQLAlchemy models (User, Task)
- routes/          Blueprints (auth, tasks)
- schemas/         Marshmallow schemas and validation helpers
migrations/        Database migration history
