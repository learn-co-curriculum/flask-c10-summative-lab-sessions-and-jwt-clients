# Summative Flask Productivity App

This repository contains a Flask reading tracker backend and two frontend clients for testing authentication flows:

- `client-with-sessions` — a session-based React client
- `client-with-jwt` — a JWT-based React client
- `Personal-reading-tracker` — the Flask API and database models

## Project purpose

The backend manages users and reading progress records. It stores a user model and a reading entry model that tracks a user’s book information, reading status, and reading session notes.

## Backend

The Flask API lives in `Personal-reading-tracker` and starts from `app.py`:

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

The Flask app listens on port `5555`.

## Data model

The backend models use SQLAlchemy:

- `User`
  - `username`
  - `email`
  - `password_hash`
  - a relationship to reading entries

- `ReadingEntry`
  - `title`
  - `author`
  - `status`
  - `rating`
  - `start_date`
  - `completion_date`
  - `user_id`

The schema layer in `schemas.py` defines Marshmallow serialization rules for the API:

- `UserSchema`
- `BookSchema`
- `ReadingSessionSchema`

The `UserSchema` fields are `id`, `username`, `email`, `password`, `created_at`, and `updated_at`.
The `BookSchema` fields are `id`, `title`, `author`, `genre`, `status`, `pages`, `current_page`, `notes`, `user_id`, `created_at`, and `updated_at`.
The `ReadingSessionSchema` fields are `id`, `book_id`, `date`, `minutes_read`, `pages_read`, `notes`, and `created_at`.

## Frontend clients

Both frontend clients are React apps that communicate with the Flask backend on `localhost:5555`.

### Sessions client

The session client in `client-with-sessions` documents the expected routes:

- `POST /login`
- `POST /signup`
- `GET /check_session`
- `DELETE /logout`

### JWT client

The JWT client in `client-with-jwt` documents the expected routes:

- `POST /login`
- `POST /signup`
- `GET /me` using a `Bearer <token>` header

## Environment note

This repository has an older Flask dependency stack that is sensitive to the Python version. The project should run with a real Python 3.11 interpreter instead of the Windows Store Python alias or Python 3.14 runtime.

## Typical workflow

1. Install the backend requirements from `requirements.txt` with a real Python 3.11 interpreter.
2. Start the Flask backend from `Personal-reading-tracker/app.py`.
3. Install and start one frontend client:
   - `npm install` then `npm start` in `client-with-sessions`, or
   - `npm install` then `npm start` in `client-with-jwt`.

## Notes

The branch name for the schema/documentation work is `Schemas-and-documentation`.
