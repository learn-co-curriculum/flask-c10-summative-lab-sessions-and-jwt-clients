# Flask JWT Notes API

A secure Flask REST API for user authentication and personal notes management. This backend supports JWT auth and a user-owned `notes` resource with full CRUD operations and pagination.

## Project Overview

- Authentication: JWT-based signup, login, and current user retrieval
- Resource: user-specific notes with `title`, `content`, and `mood`
- Authorization: users can only access their own notes
- Pagination: `GET /notes?page=1&per_page=10`

## Installation

1. Change into the backend directory:
   ```bash
   cd backend-jwt
   ```
2. Install dependencies:
   ```bash
   pipenv install
   ```

## Database Setup

1. Initialize the database and migrations:
   ```bash
   pipenv run flask db init
   pipenv run flask db migrate -m "Create users and notes"
   pipenv run flask db upgrade
   ```
2. Seed the database with example data:
   ```bash
   pipenv run python seed.py
   ```

## Running the API

Start the Flask server on port `3000`:

```bash
pipenv run python app.py
```

## Endpoints

### Auth

- `POST /signup`
  - Request: `{ "username": "string", "password": "string", "password_confirmation": "string" }`
  - Response: `{ "token": "<JWT>", "user": { "id": 1, "username": "string" } }`

- `POST /login`
  - Request: `{ "username": "string", "password": "string" }`
  - Response: `{ "token": "<JWT>", "user": { "id": 1, "username": "string" } }`

- `GET /me`
  - Header: `Authorization: Bearer <token>`
  - Response: `{ "id": 1, "username": "string" }`

### Notes Resource

- `GET /notes?page=1&per_page=10`
  - Returns current user's notes plus pagination metadata

- `POST /notes`
  - Request: `{ "title": "string", "content": "string", "mood": "string" }`
  - Creates a note for the authenticated user

- `PATCH /notes/<id>`
  - Request: `{ "title": "string", "content": "string", "mood": "string" }`
  - Updates an existing note owned by the current user

- `DELETE /notes/<id>`
  - Deletes a note owned by the current user

## Notes

- The frontend JWT client expects the API to run on `http://localhost:3000`.
- Use the `demo` user seeded in the database:
  - Username: `demo`
  - Password: `password`
