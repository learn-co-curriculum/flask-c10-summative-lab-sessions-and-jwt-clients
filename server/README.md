# Notes App – Flask API Backend

## Description
A secure Flask REST API for a personal notes app. Users sign up and log in with
session-based authentication, then create, read, update, and delete their own
notes. Passwords are hashed with Flask-Bcrypt, the notes index is paginated,
and users cannot view or modify each other's notes.

## Installation
1. Clone the repo and go into the server folder:
```
   cd server
```
2. Install dependencies and open the virtual environment:
```
   pipenv install
   pipenv shell
```
3. Set up the database:
```
   export FLASK_APP=app.py        # PowerShell: $env:FLASK_APP="app.py"
   flask db upgrade
   python seed.py
```

## Running the app
```
python app.py
```
The API runs at http://localhost:5555

Seeded users: `alice`, `bob`, `carol` (password: `password123`)

## Endpoints

### Auth
| Method | Route | Description | Success |
|---|---|---|---|
| POST | /signup | Create an account and log in | 201 |
| POST | /login | Log in | 200 |
| DELETE | /logout | Log out | 204 |
| GET | /check_session | Return the current user | 200 (401 if not logged in) |

### Notes (login required)
| Method | Route | Description | Success |
|---|---|---|---|
| GET | /notes?page=1&per_page=5 | Paginated list of your notes | 200 |
| POST | /notes | Create a note (`title`, `content`) | 201 |
| GET | /notes/<id> | Get one of your notes | 200 |
| PATCH | /notes/<id> | Update one of your notes | 200 |
| DELETE | /notes/<id> | Delete one of your notes | 204 |

Error codes: 401 not logged in, 404 note not found (or not yours), 422 validation error.

## Tech
Flask, Flask-SQLAlchemy, Flask-Migrate, Flask-RESTful, Flask-Bcrypt, Faker, pytest