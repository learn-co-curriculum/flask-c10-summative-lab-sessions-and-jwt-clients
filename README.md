# Flask Notes API

A secure RESTful Flask API backend for a personal notes management application.
Built with session-based authentication and integrated with the
`client-with-sessions` React frontend from the Summative Lab repo.

Users can register, log in, and privately manage their own notes.
Strict ownership rules are enforced — no user can view, edit, or delete
another user's notes under any circumstance.

---

## Table of Contents

- [Project Description](#project-description)
- [Features](#features)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
  - [Backend Structure](#backend-structure)
  - [Frontend Structure](#frontend-structure)
- [The Notes Resource](#the-notes-resource)
- [Installation](#installation)
- [Database Setup](#database-setup)
- [Running the Server](#running-the-server)
- [Running the Frontend](#running-the-frontend)
- [Seeding the Database](#seeding-the-database)
- [API Endpoints](#api-endpoints)
- [HTTP Status Codes](#http-status-codes)
- [Security](#security)
- [Pagination](#pagination)
- [Git Workflow](#git-workflow)
  - [Branch Strategy](#branch-strategy)
  - [Pushing the App Branch](#pushing-the-app-branch)
  - [Pushing the Models Branch](#pushing-the-models-branch)
  - [Pushing the Seed Branch](#pushing-the-seed-branch)
  - [Merging All Branches to Main](#merging-all-branches-to-main)

---

## Project Description

The Flask Notes API is a backend service that allows authenticated users to
create, read, update, and delete personal notes. Each note is privately owned
by the user who created it. No other user can access, modify, or delete
another user's notes — even if they know the note's id.

The API is built with Flask following REST principles, uses SQLite as its
development database, and implements session-based authentication using
Flask's built-in session object together with bcrypt password hashing.

The backend is designed to work with the `client-with-sessions` React
frontend from the Summative Lab repository. All error responses return an
`{ "errors": [...] }` array format to match what the frontend expects.

---

## Features

- User registration with unique username validation
- Password confirmation check during signup
- Secure password hashing with bcrypt — plain-text passwords are never stored
- Password hash protected from being read via a hybrid property exception
- Session-based login and logout
- Session check endpoint that returns 401 (not 204) so the frontend
  correctly stays on the login page when no user is logged in
- Full CRUD operations on personal notes
- Strict ownership enforcement returning 401, 403, or 404 where appropriate
- Pagination on the notes list endpoint
- All error responses use `{ "errors": [...] }` to match the frontend

---

## Tech Stack

| Package            | Version  | Purpose                          |
|--------------------|----------|----------------------------------|
| Python             | 3.8.13+  | Core language                    |
| Flask              | 2.2.2    | Web framework                    |
| Flask-SQLAlchemy   | 3.0.3    | ORM and database management      |
| Flask-Migrate      | 4.0.0    | Database schema migrations       |
| Flask-RESTful      | 0.3.9    | Resource-based API routing       |
| Flask-Bcrypt       | 1.0.1    | Password hashing                 |
| Marshmallow        | 3.20.1   | Object serialisation to JSON     |
| Werkzeug           | 2.2.2    | WSGI utilities                   |
| Faker              | 15.3.2   | Generating realistic seed data   |
| Pytest             | 7.2.0    | Testing framework                |
| SQLite             | Built-in | Development database             |

---

## Project Structure

### Backend Structure

```
flask-notes-api/
│
├── Pipfile                        # Python dependency definitions
├── Pipfile.lock                   # Locked dependency versions
├── README.md                      # Project documentation (this file)
│
└── server/                        # All backend application code
    ├── app.py                     # API resources and route registration
    │                              #   Signup, Login, Logout, CheckSession
    │                              #   NoteList, NoteDetail
    │
    ├── config.py                  # Flask app, db, bcrypt, migrate, api setup
    │                              #   All modules import from here
    │
    ├── models.py                  # SQLAlchemy models + Marshmallow schemas
    │                              #   User model (username, _password_hash)
    │                              #   Note model (title, content, user_id)
    │                              #   UserSchema, NoteSchema
    │
    ├── seed.py                    # Database seeding script
    │                              #   Creates 3 users + 5 notes each
    │
    └── instance/
        └── notes.db               # SQLite database file (auto-created)
```

---

### Frontend Structure

The frontend used is the **client-with-sessions** folder from:
[Summative Lab with Client Apps](https://github.com/learn-co-curriculum/flask-c10-summative-lab-sessions-and-jwt-clients)

```
client-with-sessions/
│
├── package.json                   # Node dependencies
├── public/
│   └── index.html                 # HTML shell
│
└── src/
    ├── index.js                   # React DOM entry point
    │
    ├── components/
    │   ├── App.js                 # Root component
    │   │                          #   GET /check_session on mount
    │   │                          #   Shows Login page or NavBar + content
    │   │
    │   ├── NavBar.js              # Top navigation bar
    │   │                          #   DELETE /logout on logout click
    │   │                          #   Clears user state on success
    │   │
    │   ├── LoginForm.js           # Login form component
    │   │                          #   POST /login with { username, password }
    │   │                          #   Reads err.errors[] for error display
    │   │
    │   └── SignUpForm.js          # Signup form component
    │                              #   POST /signup with:
    │                              #     { username, password,
    │                              #       password_confirmation }
    │                              #   Reads err.errors[] for error display
    │
    ├── pages/
    │   └── Login.js               # Login page
    │                              #   Toggles between LoginForm
    │                              #   and SignUpForm
    │
    └── styles/                    # Shared styled-components
        └── index.js               # Button, Input, Label, Error, etc.
```

---

### How the Frontend and Backend Connect

| Frontend File    | HTTP Call              | Backend Resource   | Notes |
|------------------|------------------------|--------------------|-------|
| `App.js`         | `GET /check_session`   | `CheckSession`     | Returns 401 when not logged in so `r.ok` is false and Login page is shown |
| `LoginForm.js`   | `POST /login`          | `Login`            | Sends `{ username, password }` |
| `SignUpForm.js`  | `POST /signup`         | `Signup`           | Sends `{ username, password, password_confirmation }` |
| `NavBar.js`      | `DELETE /logout`       | `Logout`           | Returns 204; `r.ok` is true so user state is cleared |
| *(future)*       | `GET /notes`           | `NoteList`         | Paginated notes list |
| *(future)*       | `POST /notes`          | `NoteList`         | Create a note |
| *(future)*       | `GET /notes/<id>`      | `NoteDetail`       | Single note |
| *(future)*       | `PATCH /notes/<id>`    | `NoteDetail`       | Update note |
| *(future)*       | `DELETE /notes/<id>`   | `NoteDetail`       | Delete note |

---

## The Notes Resource

The chosen user-owned resource is **Notes**.

A note represents a personal text entry created and owned exclusively
by one user. No other user can see or interact with it.

### Note Model Fields

| Field        | Type      | Required | Description                              |
|--------------|-----------|----------|------------------------------------------|
| `id`         | Integer   | Auto     | Primary key, auto-incremented            |
| `title`      | String    | Yes      | Short title for the note (max 200 chars) |
| `content`    | Text      | Yes      | Full note body text                      |
| `user_id`    | Integer   | Yes      | Foreign key linking to the owning user   |
| `created_at` | DateTime  | Auto     | Timestamp set automatically on creation  |
| `updated_at` | DateTime  | Auto     | Timestamp updated automatically on save  |

### Why Notes?

Notes is a natural fit for this lab because:

- It is a universally understood concept requiring no domain expertise
- It clearly demonstrates ownership — a note is always private to its author
- It has meaningful CRUD operations (create a note, read it, edit it, delete it)
- Pagination is realistic because users often accumulate many notes over time
- It maps directly to the two extra required fields: `title` and `content`

### Ownership Rules

- `GET /notes` — only returns notes where `user_id` matches the session user
- `GET /notes/<id>` — returns 403 if the note belongs to a different user
- `PATCH /notes/<id>` — returns 403 if the note belongs to a different user
- `DELETE /notes/<id>` — returns 403 if the note belongs to a different user

---

## Installation

### Prerequisites

- Python 3.8.13 or higher
- Pipenv: `pip install pipenv`
- Node.js 16+ and npm (for the frontend)

### Backend Installation

**Step 1 — Clone the repository**

```bash
git clone <your-repo-url>
cd flask-notes-api
```

**Step 2 — Install Python dependencies**

```bash
pipenv install
```

**Step 3 — Activate the virtual environment**

```bash
pipenv shell
```

**Step 4 — Navigate into the server directory**

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

A `notes.db` file will be created inside `server/instance/`.

---

## Running the Server

From inside the `server/` directory:

```bash
python app.py
```

The API starts at:

```
http://localhost:5555
```

---

## Running the Frontend

Open a **second terminal** and navigate to the frontend folder:

```bash
cd client-with-sessions
npm install
npm start
```

The frontend starts at:

```
http://localhost:3000
```

Make sure the Flask server is already running before starting the frontend.

---

## Seeding the Database

From inside the `server/` directory:

```bash
python seed.py
```

This creates 3 users (each with 5 notes) and prints the usernames to the
terminal. All seed accounts share the password `password123`.

---

## API Endpoints

### Auth Endpoints

| Method   | Endpoint          | Auth Required | Description                          |
|----------|-------------------|---------------|--------------------------------------|
| `POST`   | `/signup`         | No            | Register a new user                  |
| `POST`   | `/login`          | No            | Log in with username and password    |
| `DELETE` | `/logout`         | No            | Log out and clear the session        |
| `GET`    | `/check_session`  | No            | Return logged-in user or 401         |

---

#### `POST /signup`

Matches `SignUpForm.js` — sends `username`, `password`, `password_confirmation`.

**Request body:**
```json
{
  "username": "ash",
  "password": "pikachu123",
  "password_confirmation": "pikachu123"
}
```

**Success — 201 Created:**
```json
{ "id": 1, "username": "ash" }
```

**Error — 422 Unprocessable Entity:**
```json
{ "errors": ["That username is already taken."] }
```

---

#### `POST /login`

Matches `LoginForm.js` — sends `username` and `password`.

**Request body:**
```json
{ "username": "ash", "password": "pikachu123" }
```

**Success — 200 OK:**
```json
{ "id": 1, "username": "ash" }
```

**Error — 401 Unauthorised:**
```json
{ "errors": ["Invalid username or password."] }
```

---

#### `DELETE /logout`

Matches `NavBar.js` — checks `if (r.ok)` before clearing state.

**Success — 204 No Content:** Empty response body

---

#### `GET /check_session`

Matches `App.js` — called on mount; checks `if (r.ok)` before calling `r.json()`.

**Success — 200 OK (logged in):**
```json
{ "id": 1, "username": "ash" }
```

**Not logged in — 401 Unauthorised:**
```json
{ "errors": ["Not authenticated."] }
```

> **Why 401 and not 204?**
> `App.js` runs `r.json()` only inside `if (r.ok)`. Returning 204 (which
> is 2xx, so `r.ok = true`) would cause `r.json()` to run on an empty body
> and throw a parse error. Returning 401 makes `r.ok = false` so the
> frontend skips `r.json()` and correctly keeps `user` as null,
> showing the Login page.

---

### Notes Endpoints

All notes endpoints require the user to be logged in.
Users can only access their own notes.

| Method   | Endpoint           | Auth Required | Description                    |
|----------|--------------------|---------------|--------------------------------|
| `GET`    | `/notes`           | Yes           | Paginated list of own notes    |
| `POST`   | `/notes`           | Yes           | Create a new note              |
| `GET`    | `/notes/<id>`      | Yes           | Get a single note              |
| `PATCH`  | `/notes/<id>`      | Yes           | Update a note                  |
| `DELETE` | `/notes/<id>`      | Yes           | Delete a note                  |

---

#### `GET /notes`

**Query parameters:**

| Param      | Type    | Default | Max | Description       |
|------------|---------|---------|-----|-------------------|
| `page`     | integer | 1       | —   | Page number       |
| `per_page` | integer | 10      | 50  | Notes per page    |

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

**Error — 401:** `{ "errors": ["Unauthorised. Please log in."] }`

---

#### `POST /notes`

**Request body:**
```json
{ "title": "My note", "content": "Note content here." }
```

**Success — 201 Created:** Returns the created note object

**Errors:**
- `401` — not logged in
- `422` — missing title or content

---

#### `GET /notes/<id>`

**Success — 200 OK:** Returns the note object

**Errors:**
- `401` — not logged in
- `403` — note belongs to another user
- `404` — note not found

---

#### `PATCH /notes/<id>`

**Request body (all fields optional):**
```json
{ "title": "Updated title", "content": "Updated content." }
```

**Success — 200 OK:** Returns the updated note object

**Errors:**
- `401` — not logged in
- `403` — note belongs to another user
- `404` — note not found
- `422` — title or content provided but empty

---

#### `DELETE /notes/<id>`

**Success — 204 No Content:** Empty response body

**Errors:**
- `401` — not logged in
- `403` — note belongs to another user
- `404` — note not found

---

## HTTP Status Codes

| Code  | Meaning               | When Returned                                        |
|-------|-----------------------|------------------------------------------------------|
| `200` | OK                    | Successful GET, PATCH, login, check_session          |
| `201` | Created               | Successful signup or POST /notes                     |
| `204` | No Content            | Successful DELETE or logout                          |
| `401` | Unauthorised          | Not logged in, or check_session with no session      |
| `403` | Forbidden             | Logged in but does not own the resource              |
| `404` | Not Found             | The requested note does not exist                    |
| `422` | Unprocessable Entity  | Missing or invalid fields in the request body        |

---

## Security

**Password hashing**
All passwords are hashed with bcrypt before being stored in the database.
The plain-text password is never persisted anywhere.

**Password read protection**
The `password_hash` hybrid property raises an `Exception` if anything
tries to read it, preventing accidental serialisation or logging of hashes.

**Password confirmation**
The signup endpoint validates that `password` and `password_confirmation`
match before creating any account.

**Session encryption**
Flask signs session cookies using the app `secret_key`, preventing
clients from tampering with session data.

**Ownership enforcement**
Every notes endpoint verifies that the note's `user_id` matches the
logged-in user's `id`. Mismatches return `403 Forbidden`.

**Database-level uniqueness**
The `username` column has `unique=True` at the database level, preventing
duplicate usernames even if application-level validation is bypassed.

**Cross-user data isolation**
`GET /notes` uses `filter_by(user_id=user.id)` at the SQL level, so
manipulating pagination parameters can never expose another user's notes.

**Error format consistency**
All errors return `{ "errors": [...] }` as an array, matching the pattern
the frontend uses to display multiple validation messages at once.

---

## Pagination

`GET /notes` returns notes in pages to avoid large single payloads.

**Parameters:**
- `page` — which page to return (starts at 1, default 1)
- `per_page` — items per page (default 10, maximum 50)

**Metadata returned with every paginated response:**

| Field          | Type    | Description                              |
|----------------|---------|------------------------------------------|
| `total`        | integer | Total notes owned by the logged-in user  |
| `pages`        | integer | Total number of pages available          |
| `current_page` | integer | Page number returned in this response    |
| `per_page`     | integer | Number of notes per page                 |
| `has_next`     | boolean | Whether a next page exists               |
| `has_prev`     | boolean | Whether a previous page exists           |

---

## Git Workflow

This project uses **three feature branches** — one for each major file —
before merging everything into `main`.

```
main
├── feature/app        ← app.py (API resources and routes)
├── feature/models     ← models.py (User and Note models)
└── feature/seed       ← seed.py (database seeding script)
```

---

### Branch Strategy

| Branch           | File(s) Owned           | Purpose                          |
|------------------|-------------------------|----------------------------------|
| `feature/app`    | `server/app.py`         | All API resources and endpoints  |
| `feature/models` | `server/models.py`      | User, Note models and schemas    |
| `feature/seed`   | `server/seed.py`        | Database seeding logic           |
| `main`           | Everything merged       | Final production-ready code      |

---

### Initial Setup (Do This Once)

Before creating any branches, set up the repository:

```bash
# Navigate to your project folder
cd flask-notes-api

# Initialise git if not already done
git init

# Add all files and make the first commit on main
git add .
git commit -m "Initial project setup — config, Pipfile, README"

# Connect to your GitHub repository
git remote add origin https://github.com/<your-username>/<your-repo>.git

# Push main to GitHub
git push -u origin main
```

---

### Pushing the App Branch

This branch contains `server/app.py` — all API resources and route registration.

**Step 1 — Make sure you are on main and it is up to date**
```bash
git checkout main
git pull origin main
```

**Step 2 — Create and switch to the app feature branch**
```bash
git checkout -b feature/app
```

**Step 3 — Make your changes to app.py, then stage only that file**
```bash
git add server/app.py
```

**Step 4 — Verify only app.py is staged**
```bash
git status
```

**Step 5 — Commit with a descriptive message**
```bash
git commit -m "Add API resources: Signup, Login, Logout, CheckSession, NoteList, NoteDetail"
```

**Step 6 — Push the branch to GitHub**
```bash
git push origin feature/app
```

**Step 7 — Open a Pull Request on GitHub**

- Go to your repository on GitHub
- Click **Compare & pull request** next to `feature/app`
- Set base branch to `main`
- Title: `feat: Add all API resources and route registration`
- Add a description of what endpoints were added
- Click **Create pull request**

---

### Pushing the Models Branch

This branch contains `server/models.py` — the User and Note models
plus their Marshmallow schemas.

**Step 1 — Go back to main and pull the latest changes**
```bash
git checkout main
git pull origin main
```

**Step 2 — Create and switch to the models feature branch**
```bash
git checkout -b feature/models
```

**Step 3 — Make your changes to models.py, then stage it**
```bash
git add server/models.py
```

**Step 4 — Verify only models.py is staged**
```bash
git status
```

**Step 5 — Commit with a descriptive message**
```bash
git commit -m "Add User and Note models with bcrypt password protection and Marshmallow schemas"
```

**Step 6 — Push the branch to GitHub**
```bash
git push origin feature/models
```

**Step 7 — Open a Pull Request on GitHub**

- Go to your repository on GitHub
- Click **Compare & pull request** next to `feature/models`
- Set base branch to `main`
- Title: `feat: Add User and Note SQLAlchemy models and schemas`
- Add a description of the models, fields, and relationships
- Click **Create pull request**

---

### Pushing the Seed Branch

This branch contains `server/seed.py` — the database seeding script.

**Step 1 — Go back to main and pull the latest changes**
```bash
git checkout main
git pull origin main
```

**Step 2 — Create and switch to the seed feature branch**
```bash
git checkout -b feature/seed
```

**Step 3 — Make your changes to seed.py, then stage it**
```bash
git add server/seed.py
```

**Step 4 — Verify only seed.py is staged**
```bash
git status
```

**Step 5 — Commit with a descriptive message**
```bash
git commit -m "Add seed script: creates 3 users and 5 notes each for development testing"
```

**Step 6 — Push the branch to GitHub**
```bash
git push origin feature/seed
```

**Step 7 — Open a Pull Request on GitHub**

- Go to your repository on GitHub
- Click **Compare & pull request** next to `feature/seed`
- Set base branch to `main`
- Title: `feat: Add database seed script for User and Note models`
- Add a description of what data is seeded
- Click **Create pull request**

---

### Merging All Branches to Main

After each Pull Request has been reviewed, merge them into main one at a time.

---

#### Merge feature/app into main

**On GitHub:**

- Open the `feature/app` Pull Request
- Review the changes in the **Files changed** tab
- Click **Merge pull request**
- Click **Confirm merge**
- Click **Delete branch** to keep the repo clean

**Then update your local main:**
```bash
git checkout main
git pull origin main
```

---

#### Merge feature/models into main

**On GitHub:**

- Open the `feature/models` Pull Request
- If GitHub shows a merge conflict, resolve it first (see below)
- Click **Merge pull request**
- Click **Confirm merge**
- Click **Delete branch**

**Then update your local main:**
```bash
git checkout main
git pull origin main
```

---

#### Merge feature/seed into main

**On GitHub:**

- Open the `feature/seed` Pull Request
- Click **Merge pull request**
- Click **Confirm merge**
- Click **Delete branch**

**Then update your local main:**
```bash
git checkout main
git pull origin main
```

---

#### Verify the Final State of Main

After all three branches are merged, confirm everything is on main:

```bash
git checkout main
git pull origin main
ls server/
```

You should see:
```
app.py   config.py   models.py   seed.py   instance/
```

**Make a final commit if any loose files were not yet included:**
```bash
git add .
git commit -m "Final: all features merged — auth, models, seed, CRUD, pagination"
git push origin main
```

---

#### Resolving Merge Conflicts

If GitHub reports a conflict when merging a branch:

**Step 1 — Switch to the conflicting branch locally**
```bash
git checkout feature/models
```

**Step 2 — Pull the latest main into the branch**
```bash
git pull origin main
```

**Step 3 — Git will mark conflicted files. Open each one and look for:**
```
<<<<<<< HEAD
your branch code
=======
main branch code
>>>>>>> main
```

**Step 4 — Edit the file to keep the correct code and remove the markers**

**Step 5 — Stage and commit the resolved file**
```bash
git add server/models.py
git commit -m "Resolve merge conflict in models.py"
```

**Step 6 — Push the resolved branch**
```bash
git push origin feature/models
```

**Step 7 — Return to GitHub and complete the merge**

---

### Full Branch Command Reference

| Action                          | Command                                           |
|---------------------------------|---------------------------------------------------|
| Create and switch to a branch   | `git checkout -b feature/<name>`                  |
| Switch to an existing branch    | `git checkout feature/<name>`                     |
| Stage a specific file           | `git add server/<filename>.py`                    |
| Check what is staged            | `git status`                                      |
| Commit with a message           | `git commit -m "your message"`                    |
| Push a branch to GitHub         | `git push origin feature/<name>`                  |
| Update local main after merge   | `git checkout main && git pull origin main`       |
| List all local branches         | `git branch`                                      |
| List all remote branches        | `git branch -r`                                   |
| Delete a local branch           | `git branch -d feature/<name>`                    |