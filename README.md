# Flask Notes API

A secure RESTful Flask API backend for a personal notes application.
Users can register, log in, and privately manage their own notes.
Strict ownership rules are enforced — no user can view, edit, or
delete another user's data under any circumstance.

Authentication method: **Session-based** (use the `sessions-client`
folder from the provided frontend repo).

---

## Table of Contents

- [Project Description](#project-description)
- [Features](#features)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [Installation](#installation)
- [Database Setup](#database-setup)
- [Running the Server](#running-the-server)
- [Seeding the Database](#seeding-the-database)
- [API Endpoints](#api-endpoints)
- [HTTP Status Codes](#http-status-codes)
- [Security](#security)
- [Pagination](#pagination)
- [Frontend Integration](#frontend-integration)
- [Git Workflow](#git-workflow)

---

## Project Description

The Flask Notes API is a backend service that allows authenticated
users to create, read, update, and delete personal notes. Each note
is privately owned by the user who created it. No other user can
access, modify, or delete another user's notes — even if they know
the note's id.

The API is built with Flask following REST principles. It uses SQLite
as its development database and implements session-based
authentication using Flask's built-in session object together with
bcrypt password hashing.

---

## Features

- User registration with unique username and email validation
- Secure password hashing using bcrypt — plain-text passwords are never stored
- Password hash protected from being read directly via a hybrid property
- Session-based login and logout
- Session check endpoint to restore authenticated state on page reload
- Full CRUD operations for personal notes
- Strict ownership enforcement on every notes endpoint
- Pagination on the notes list endpoint with configurable page size
- Descriptive error messages and correct HTTP status codes on every route
- Database seeding script for development and manual testing

---

## Tech Stack

| Package | Version | Purpose |
|---|---|---|
| Python | 3.8.13+ | Core language |
| Flask | 2.2.2 | Web framework |
| Flask-SQLAlchemy | 3.0.3 | ORM and database management |
| Flask-Migrate | 4.0.0 | Database schema migrations |
| Flask-RESTful | 0.3.9 | Resource-based API routing |
| Flask-Bcrypt | 1.0.1 | Password hashing |
| Marshmallow | 3.20.1 | Object serialisation to JSON |
| Werkzeug | 2.2.2 | WSGI utilities |
| Faker | 15.3.2 | Generating realistic seed data |
| Pytest | 7.2.0 | Testing framework |
| SQLite | Built-in | Development database |

---

## Project Structure

```
flask-notes-api/
│
├── Pipfile                  # Python dependency definitions
├── Pipfile.lock             # Locked dependency versions
├── README.md                # Project documentation
│
└── server/                  # All backend application code
    ├── app.py               # API resources and route registration
    ├── config.py            # App, db, bcrypt, migrate, api initialisation
    ├── models.py            # SQLAlchemy models and Marshmallow schemas
    ├── seed.py              # Database seeding script
    └── instance/
        └── notes.db         # SQLite database (auto-created)
```

---

## Installation

### Prerequisites

- Python 3.8.13 or higher
- Pipenv (`pip install pipenv`)

### Steps

**1. Clone the repository**

```bash
git clone <your-repo-url>
cd flask-notes-api
```

**2. Install all Python dependencies**

```bash
pipenv install
```

**3. Activate the virtual environment**

```bash
pipenv shell
```

**4. Navigate to the server directory**

```bash
cd server
```

---

## Database Setup

Run these commands from inside the `server/` directory:

```bash
# Initialise the migrations folder (only needed once)
flask db init

# Generate a migration file from the current models
flask db migrate -m "initial migration"

# Apply the migration to create all database tables
flask db upgrade head
```

After running these commands, a `notes.db` file will be created
inside `server/instance/`.

---

## Running the Server

From inside the `server/` directory:

```bash
python app.py
```

The API will be available at:

```
http://localhost:5555
```

---

## Seeding the Database

Populate the database with 3 sample users and 15 sample notes:

```bash
python seed.py
```

The terminal will print all created usernames and emails.
All seed accounts share the password: `password123`

---

## API Endpoints

### Auth Endpoints

| Method | Endpoint | Auth Required | Description |
|---|---|---|---|
| POST | `/signup` | No | Register a new user |
| POST | `/login` | No | Log in with username and password |
| DELETE | `/logout` | No | Log out and clear the session |
| GET | `/check_session` | No | Return logged-in user or 204 |

---

#### `POST /signup`

**Request body:**
```json
{
  "username": "ash",
  "email": "ash@example.com",
  "password": "pikachu123"
}
```

**Success — 201 Created:**
```json
{ "id": 1, "username": "ash", "email": "ash@example.com" }
```

**Errors:** `422` missing fields · `422` username taken · `422` email taken

---

#### `POST /login`

**Request body:**
```json
{ "username": "ash", "password": "pikachu123" }
```

**Success — 200 OK:**
```json
{ "id": 1, "username": "ash", "email": "ash@example.com" }
```

**Errors:** `401` invalid credentials

---

#### `DELETE /logout`

**Success — 204 No Content:** Empty response body

---

#### `GET /check_session`

**Success — 200 OK (logged in):**
```json
{ "id": 1, "username": "ash", "email": "ash@example.com" }
```

**Not logged in — 204 No Content:** Empty response body

---

### Notes Endpoints

All notes endpoints require the user to be logged in.
Users can only access notes they personally created.

| Method | Endpoint | Auth Required | Description |
|---|---|---|---|
| GET | `/notes` | Yes | Paginated list of own notes |
| POST | `/notes` | Yes | Create a new note |
| GET | `/notes/<id>` | Yes | Get a single note |
| PATCH | `/notes/<id>` | Yes | Update a note |
| DELETE | `/notes/<id>` | Yes | Delete a note |

---

#### `GET /notes`

**Query parameters:**

| Param | Type | Default | Max | Description |
|---|---|---|---|---|
| `page` | integer | 1 | — | Page number |
| `per_page` | integer | 10 | 50 | Notes per page |

**Example:** `GET /notes?page=1&per_page=5`

**Success — 200 OK:**
```json
{
  "notes": [
    {
      "id": 1,
      "title": "Buy groceries",
      "content": "Milk, eggs, bread.",
      "user_id": 1,
      "created_at": "2024-07-01T10:30:00",
      "updated_at": "2024-07-01T10:30:00"
    }
  ],
  "total": 12,
  "pages": 3,
  "current_page": 1,
  "per_page": 5,
  "has_next": true,
  "has_prev": false
}
```

**Errors:** `401` not logged in

---

#### `POST /notes`

**Request body:**
```json
{ "title": "My note", "content": "Note content here." }
```

**Success — 201 Created:** Returns the created note object

**Errors:** `401` not logged in · `422` missing title or content

---

#### `GET /notes/<id>`

**Success — 200 OK:** Returns the note object

**Errors:** `401` not logged in · `403` not your note · `404` not found

---

#### `PATCH /notes/<id>`

**Request body (all fields optional):**
```json
{ "title": "New title", "content": "New content." }
```

**Success — 200 OK:** Returns the updated note object

**Errors:** `401` not logged in · `403` not your note · `404` not found · `422` empty field

---

#### `DELETE /notes/<id>`

**Success — 204 No Content:** Empty response body

**Errors:** `401` not logged in · `403` not your note · `404` not found

---

## HTTP Status Codes

| Code | Meaning | When Returned |
|---|---|---|
| `200` | OK | Successful GET, PATCH, login, check_session |
| `201` | Created | Successful signup or POST /notes |
| `204` | No Content | Successful DELETE, logout, or unauthenticated check_session |
| `401` | Unauthorised | User is not logged in |
| `403` | Forbidden | User is logged in but does not own the resource |
| `404` | Not Found | The requested note does not exist |
| `422` | Unprocessable Entity | Missing or invalid fields in the request |

---

## Security

**Password hashing**
All passwords are hashed with bcrypt before being stored.
The plain-text password is never saved and cannot be retrieved.

**Password read protection**
The `password_hash` hybrid property raises an Exception if anything
tries to read it, preventing accidental serialisation or logging.

**Session encryption**
Flask signs session cookies using the app's `secret_key`, preventing
clients from tampering with session data.

**Ownership enforcement**
Every notes endpoint verifies that the note's `user_id` matches the
logged-in user's `id`. A `403 Forbidden` is returned on mismatch.

**Database-level uniqueness**
The `username` and `email` columns both have `unique=True` at the
database level, preventing duplicates even if the application
validation is bypassed.

**Cross-user data isolation**
`GET /notes` filters at the SQL level using `filter_by(user_id=user.id)`,
so a user can never retrieve another user's notes by manipulating
pagination parameters.

---

## Pagination

`GET /notes` supports pagination to avoid returning large payloads.

**Parameters:** `page` (default 1) and `per_page` (default 10, max 50)

**Metadata returned in every paginated response:**

| Field | Type | Description |
|---|---|---|
| `total` | integer | Total notes owned by the user |
| `pages` | integer | Total pages available |
| `current_page` | integer | The page returned in this response |
| `per_page` | integer | Notes per page |
| `has_next` | boolean | Whether a next page exists |
| `has_prev` | boolean | Whether a previous page exists |

---

## Frontend Integration

Use the **sessions-client** folder from the
[Summative Lab repo](https://github.com/learn-co-curriculum/flask-c10-summative-lab-sessions-and-jwt-clients).

```bash
# In a second terminal
cd sessions-client
npm install
npm start
```

Frontend runs on `http://localhost:3000`.
Make sure the Flask server is already running on port `5555`.

---

## Git Workflow

```bash
# Create a feature branch
git checkout -b feature/notes-api

# Stage and commit your changes regularly
git add .
git commit -m "Add Note model and CRUD endpoints"

# Push the branch to GitHub
git push origin feature/notes-api

# Open a Pull Request on GitHub, review, then merge to main
# After merging, update your local main branch
git checkout main
git pull origin main
```