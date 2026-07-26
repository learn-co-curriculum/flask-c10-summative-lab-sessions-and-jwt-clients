# FocusFlaw API

## Project Description

FocusFlaw API is a Flask RESTful backend that allows users to securely manage their personal tasks. Users can create an account, log in using session-based authentication, and perform CRUD operations on their own tasks.

The application ensures that users can only access and modify tasks that belong to them. Passwords are securely hashed before being stored in the database.

---

## Features

- User registration
- User login
- Session-based authentication
- Logout
- Session verification
- Create tasks
- View personal tasks
- Update tasks
- Delete tasks
- Pagination for task listing
- Password hashing with Flask-Bcrypt
- Database migrations using Flask-Migrate
- Marshmallow serialization

---

## Technologies Used

- Python 3
- Flask
- Flask-SQLAlchemy
- Flask-Migrate
- Flask-Bcrypt
- Marshmallow
- SQLite
- SQLAlchemy

---

## Installation

Clone the repository:

```bash
git clone <repository-url>
cd focusflaw_api
```

Install dependencies:

```bash
pipenv install
```

Activate the virtual environment:

```bash
pipenv shell
```

---

## Configure the Database

Initialize migrations (only once if needed):

```bash
flask db init
```

Generate a migration:

```bash
flask db migrate -m "Initial migration"
```

Apply migrations:

```bash
flask db upgrade
```

---

## Running the Application

Start the Flask server:

```bash
python app.py
```

The server runs on:

```
http://127.0.0.1:5555
```

---

## Authentication

This project uses **Flask Sessions** for authentication.

After a successful login or signup, a session cookie is stored by the browser/client.

Protected endpoints require an active session.

---

# API Endpoints

## Home

### GET /

Returns a welcome message.

---

## Authentication

### POST /signup

Create a new user account.

Request

```json
{
    "username": "Ryan",
    "email": "ryan@example.com",
    "password": "12345"
}
```

Response

```json
{
    "id": 1,
    "username": "Ryan",
    "email": "ryan@example.com"
}
```

---

### POST /login

Authenticate an existing user.

Request

```json
{
    "username": "Ryan",
    "password": "12345"
}
```

---

### GET /check_session

Returns the currently authenticated user.

---

### DELETE /logout

Logs out the current user.

---

# Task Endpoints

## GET /tasks

Returns the logged-in user's tasks.

Supports pagination.

Example:

```
GET /tasks?page=1
```

---

## POST /tasks

Creates a new task.

Request

```json
{
    "title": "Finish Moringa Lab",
    "description": "Complete backend project"
}
```

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

Deletes a task.

---

## Database Models

### User

- id
- username
- email
- password_hash
- created_at
- updated_at

Relationship:

- One User has many Tasks.

---

### Task

- id
- title
- description
- completed
- created_at
- updated_at
- user_id

Relationship:

- Each Task belongs to one User.

---

## Project Structure

```
focusflaw_api/

├── app.py
├── config.py
├── extensions.py
├── seed.py
├── models/
│   ├── user.py
│   ├── task.py
│   └── __init__.py
│
├── schemas/
│   ├── user_schema.py
│   ├── task_schema.py
│   └── __init__.py
│
├── resources/
│   ├── auth.py
│   └── task.py
│
├── migrations/
├── instance/
└── Pipfile
```

---

## Testing

The API was tested using the VS Code Postman extension.

Verified functionality:

- User signup
- User login
- Session persistence
- Session logout
- Task creation
- Task retrieval
- Task updating
- Task deletion
- Authorization
- Pagination

---