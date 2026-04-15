# Productivity App Backend

This is a Flask API for a productivity app. It has user login with JWT and lets users create, read, update, and delete their own notes.

## How to Install

1. Install the stuff needed:
   ```
   pipenv install
   ```

2. Set up the database:
   ```
   pipenv run flask db init
   pipenv run flask db migrate -m "initial"
   pipenv run flask db upgrade
   ```

3. Add some sample data:
   ```
   pipenv run python seed.py
   ```

## How to Run

```
pipenv run flask run
```

The app will be at http://localhost:5000.

## API Endpoints

### For Authentication

- **POST /signup**
  - Send: `{"username": "yourname", "password": "yourpass"}`
  - Gets back: `{"token": "jwt-token", "user": {...}}` or error

- **POST /login**
  - Send: `{"username": "yourname", "password": "yourpass"}`
  - Gets back: `{"token": "jwt-token", "user": {...}}` or error

- **POST /logout**
  - Logs out the current user
  - Gets back: `{"message": "Logged out"}`

- **GET /me**
  - Headers: `Authorization: Bearer <token>`
  - Gets back: user info or error

### For Notes

All these require JWT token in Authorization header: `Authorization: Bearer <token>`.

- **GET /notes**
  - Can add ?page=1&per_page=10
  - Gets back: list of notes with paging info

- **POST /notes**
  - Send: `{"title": "mytitle", "content": "mycontent"}`
  - Gets back: the new note

- **GET /notes/<id>**
  - Gets back: one note or error

- **PATCH /notes/<id>**
  - Send: `{"title": "newtitle"}` or whatever to change
  - Gets back: updated note

- **DELETE /notes/<id>**
  - Gets back: `{"message": "Note deleted"}`