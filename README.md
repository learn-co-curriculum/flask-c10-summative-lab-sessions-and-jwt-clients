# Productivity Notes API

A secure Flask REST API backend for a personal notes app. Users can sign up, log
in, and manage their own notes (create, read, update, delete) with pagination.
Authentication is **session-based** (Flask sessions + cookies), and passwords are
hashed with **Flask-Bcrypt**. Users can only ever see or change their own notes.

It is built to work with the provided `client-with-sessions` React frontend.

## Tech Stack

Flask, Flask-RESTful, Flask-SQLAlchemy, Flask-Migrate, Flask-Bcrypt, Marshmallow, Faker, SQLite.

## Project Structure

```
.
├── app.py              # entry point, registers routes
├── config.py           # Flask app + extensions (db, migrate, bcrypt, api)
├── models.py           # User and Note models
├── schemas.py          # Marshmallow validation/serialization
├── utils.py            # login_required decorator, error formatting
├── seed.py             # demo data
├── resources/
│   ├── auth.py         # signup, login, logout, check_session
│   └── notes.py        # protected CRUD + pagination for notes
├── migrations/         # Flask-Migrate files
└── Pipfile
```

## Installation

Requires Python 3.8+ and [Pipenv](https://pipenv.pypa.io/).

```bash
git clone <your-repo-url>
cd <your-repo-folder>

pipenv install
pipenv shell

# create and apply the database migrations
# (skip `flask db init` if the migrations/ folder already exists)
export FLASK_APP=app.py
flask db init
flask db migrate -m "create users and notes"
flask db upgrade

# seed demo data
python seed.py
```

Seeded users: `alice`, `bob`, `charlie`, all with password `password123`
(each has 15 notes, so pagination is easy to see).

## Running the Server

```bash
flask run -p 5555
# or
python app.py
```

The API runs at `http://localhost:5555`. To use the frontend, run
`npm install && npm start` inside `client-with-sessions/`; its proxy points to port 5555.

## API Endpoints

All responses are JSON. Errors look like `{"errors": ["message", ...]}`.

### Authentication

| Method | Endpoint         | Description | Success | Errors |
|--------|------------------|-------------|---------|--------|
| POST   | `/signup`        | Create a user and log them in. Body: `username`, `password`, `password_confirmation`. Username must be unique (3+ chars); password 6+ chars. | 201 + user | 422 |
| POST   | `/login`         | Log in with `username` and `password`; sets the session cookie. | 200 + user | 401 |
| DELETE | `/logout`        | Log out (clears the session). | 204 | - |
| GET    | `/check_session` | Return the logged-in user (used to stay logged in on refresh). | 200 + user | 401 `{}` |

### Notes (login required)

A request without a valid session gets **401**. Trying to access another user's
note gets **403**; a note that does not exist gets **404**.

| Method | Endpoint        | Description | Success | Errors |
|--------|-----------------|-------------|---------|--------|
| GET    | `/notes`        | Paginated list of the current user's notes. Query: `page` (default 1), `per_page` (default 10, max 100). Pinned notes come first, then newest. | 200 | 400, 401 |
| POST   | `/notes`        | Create a note. Body: `title` (required), `content` (required), `category` (optional), `is_pinned` (optional). | 201 + note | 401, 422 |
| GET    | `/notes/<id>`   | Get one of your notes. | 200 + note | 401, 403, 404 |
| PATCH  | `/notes/<id>`   | Update any of `title`, `content`, `category`, `is_pinned`. | 200 + note | 400, 401, 403, 404, 422 |
| DELETE | `/notes/<id>`   | Delete one of your notes. | 204 | 401, 403, 404 |

Paginated response shape for `GET /notes`:

```json
{
  "notes": [{"id": 1, "title": "...", "content": "...", "category": "work",
             "is_pinned": false, "created_at": "...", "updated_at": "...", "user_id": 1}],
  "page": 1, "per_page": 10, "total": 15, "pages": 2,
  "has_next": true, "has_prev": false
}
```

## Quick Test with curl

```bash
# log in and keep the session cookie
curl -i -c cookies.txt -H "Content-Type: application/json" \
  -d '{"username":"alice","password":"password123"}' http://localhost:5555/login

# list notes (page 2, 5 per page)
curl -b cookies.txt "http://localhost:5555/notes?page=2&per_page=5"

# create a note
curl -b cookies.txt -H "Content-Type: application/json" \
  -d '{"title":"Hello","content":"My first note"}' http://localhost:5555/notes

# without the cookie -> 401
curl -i http://localhost:5555/notes
```

## Notes

- Set `SECRET_KEY` (and optionally `DATABASE_URI`) as environment variables in production.