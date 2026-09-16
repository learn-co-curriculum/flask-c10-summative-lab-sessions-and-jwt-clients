# Productivity Tracker API

This project is a secure Flask backend for a productivity tool that lets users manage personal notes. It uses JWT authentication to protect user-specific data and ensures that each user can only access and modify their own notes.

## Features

- User signup and login with secure password hashing
- JWT-based authentication and user session validation via `/me`
- Protected notes resource with full CRUD support
- Access control so users only see their own notes
- Pagination on the notes index route
- Database migrations with Flask-Migrate
- Seed data for quick local setup

## Installation

1. Clone the repository.
2. Change into the project directory.
3. Install dependencies with Pipenv:

```bash
pipenv install
```

4. Activate the virtual environment:

```bash
pipenv shell
```

5. Run database migrations:

```bash
flask db init
flask db migrate -m "initial migration"
flask db upgrade
```

6. Seed the database:

```bash
python seed.py
```

## Run the app

```bash
flask run
```

The API will be available at `http://localhost:5000`.

## Authentication Endpoints

### `POST /signup`
Creates a new user account and returns a JWT token.

Request body:

```json
{
  "username": "alice",
  "password": "password123",
  "password_confirmation": "password123"
}
```

### `POST /login`
Logs in an existing user and returns a JWT token.

Request body:

```json
{
  "username": "alice",
  "password": "password123"
}
```

### `GET /me`
Returns the current authenticated user.

Headers:

```http
Authorization: Bearer <token>
```

## Notes Endpoints

### `GET /notes?page=1&per_page=10`
Returns the current user's notes with pagination.

Headers:

```http
Authorization: Bearer <token>
```

### `POST /notes`
Creates a new note for the logged-in user.

Request body:

```json
{
  "title": "Morning plan",
  "content": "Review the latest priorities before lunch."
}
```

### `PATCH /notes/<id>`
Updates an existing note owned by the current user.

### `DELETE /notes/<id>`
Deletes a note owned by the current user.

## Notes Model

Each note includes:

- `id`
- `title`
- `content`
- `user_id`
- `created_at`
- `updated_at`

The notes table is associated with the user table through a foreign key so users cannot access each other's data.
