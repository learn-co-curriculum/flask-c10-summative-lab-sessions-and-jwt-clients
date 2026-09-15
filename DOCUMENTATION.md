# Summative Flask Productivity App Documentation

## Project Description

This repository contains a Flask reading tracker API with a session-based frontend client and a JWT-based frontend client. The backend stores users and reading records for a personal reading tracker. It is designed so that a user can create an account, sign in, manage their own reading entries, and track reading progress.

The backend project lives in the nested folder `Personal-reading-tracker` and uses Flask, SQLAlchemy, Flask-Migrate, Marshmallow, Flask-RESTful, and Flask-Bcrypt.

## Repository Structure

- `Personal-reading-tracker/app.py` — Flask application entrypoint.
- `Personal-reading-tracker/models.py` — SQLAlchemy database model definitions.
- `Personal-reading-tracker/schemas.py` — Marshmallow schema definitions.
- `Personal-reading-tracker/seed.py` — seed data utilities.
- `client-with-sessions/` — session auth frontend client.
- `client-with-jwt/` — JWT auth frontend client.

## Backend Setup

The backend dependency versions are pinned in `requirements.txt`:

```text
flask==2.2.2
flask-sqlalchemy==3.0.3
Werkzeug==2.2.2
marshmallow==3.20.1
faker==15.3.2
flask-migrate==4.0.0
flask-restful==0.3.9
importlib-metadata==6.0.0
importlib-resources==5.10.0
pytest==7.2.0
flask-bcrypt==1.0.1
```

Use a real Python 3.11 interpreter. The older Flask stack is sensitive to the Python 3.14 and Windows Store alias behavior.

## Backend Startup

The app entrypoint runs the Flask server on port `5555`:

```python
from flask import Flask
from flask_migrate import Migrate

from models import db

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
migrate = Migrate(app, db)

if __name__ == '__main__':
    app.run(port=5555, debug=True)
```

## Data Models

### User

The SQLAlchemy `User` model has the following fields:

- `id` — integer primary key
- `username` — unique string, required
- `email` — unique string, required
- `password_hash` — string, required
- `reading_entries` — relationship to reading records

### ReadingEntry

The SQLAlchemy `ReadingEntry` model has the following fields:

- `id` — integer primary key
- `title` — required string
- `author` — required string
- `status` — required string, default `want_to_read`
- `rating` — optional integer
- `start_date` — optional date
- `completion_date` — optional date
- `user_id` — required foreign key to `users.id`

## Marshmallow Schemas

The `schemas.py` file defines the serializer contracts:

### UserSchema

Fields:

- `id` — integer, dump only
- `username` — required string, length between 3 and 80
- `email` — required email field
- `password` — required string, load only, minimum length 6
- `created_at` — dump only date-time
- `updated_at` — dump only date-time

### BookSchema

Fields:

- `id` — integer, dump only
- `title` — required string, length 1-200
- `author` — required string, length 1-200
- `genre` — optional string
- `status` — required, allowed values `want_to_read`, `reading`, `finished`
- `pages` — required integer, minimum 1
- `current_page` — integer, default 0, minimum 0
- `notes` — optional string
- `user_id` — required integer
- `created_at` — dump only date-time
- `updated_at` — dump only date-time

### ReadingSessionSchema

Fields:

- `id` — integer, dump only
- `book_id` — required integer
- `date` — required date
- `minutes_read` — required integer, minimum 1
- `pages_read` — required integer, minimum 0
- `notes` — optional string
- `created_at` — dump only date-time

## Frontend API Contract

### Session frontend client

The session-based client in `client-with-sessions` expects the backend to implement:

- `POST /login`
- `POST /signup`
- `GET /check_session`
- `DELETE /logout`

It expects JSON responses and Flask sessions.

### JWT frontend client

The JWT-based client in `client-with-jwt` expects the backend to implement:

- `POST /login`
- `POST /signup`
- `GET /me` using a `Authorization: Bearer <token>` header

It expects JSON responses and a JWT token returned on signup/login.

## Authentication

The project supports both session-based and JWT-based authentication patterns by contract. The repository includes `auth.py` and `auth_schemas.py` in the merged `main` branch baseline and the tests in `tests/test_auth.py` demonstrate the authentication route expectations.

## Developer Notes

The repository should be run from a real Python 3.11 interpreter. The workspace command path may otherwise resolve `python` or `py` to the Microsoft Store alias, which points at a stub and causes mismatched environment behavior.
