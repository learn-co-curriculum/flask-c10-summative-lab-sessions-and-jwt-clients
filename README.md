# Flask JWT Notes API

This project builds a secure Flask API for managing personal notes. Users can sign up, log in, and create, view, update, and delete only their own notes.

## Setup

1. Install dependencies:
   ```bash
   pipenv install
   ```

2. Create the database:
   ```bash
   pipenv run flask db init
   pipenv run flask db migrate -m "initial migration"
   pipenv run flask db upgrade
   ```

3. Seed sample data:
   ```bash
   pipenv run python seed.py
   ```

## Run the API

```bash
pipenv run python app.py
```

The server will run on http://localhost:5555.

## Endpoints

### Authentication
- POST /signup
- POST /login
- GET /me

### Notes
- GET /notes?page=1&per_page=10
- POST /notes
- PATCH /notes/<id>
- DELETE /notes/<id>

## Notes on access control

Each note belongs to a single user. Requests are tied to the current authenticated user through JWTs, so one user cannot view or modify another user's notes.
