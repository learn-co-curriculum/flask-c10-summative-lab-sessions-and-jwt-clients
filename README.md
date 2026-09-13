# FLASK JWT Auth
A secure REST API built with flask, SQLAlchemy and Flask-JWT-Extended. Users can register,login and manage personal notes with JWT protection.

## Features
1. User Registration & Login with bcrypt hashing
2. JWT Authentication(Bearer Token)
3. Protected Routes `/protected` and `/notes`

## Tech Stack
 - Flask, Flask-SQLAlchemy, Flask-Migrate, Flask-Bcrypt, Flask-JWT-Extended, Flask-CORS
 - Gunicorn for production
 - SQLite locally / PostgreSQL in production

 ## Local Setup
 1. Install
 pipenv install
 pipenv shell
 2. Setup DB
 flask --app app db init
 flask --app app db migrate -m "initial"
 flask --app app db upgrade
 python seed.py
 3. Run
 flask --app app run --port=5000 --debug
  server on http://127.0.0.1:5000

## API Endpoints
METHOD          ENDPOINT            AUTH        DESCRIPTION
POST            /register             No        {"username", "email", "password"}
POST            /login                No        {"username", "password"} -> {"access_token"}
GET             /me                   Yes       Get current user
GET             /notes                Yes       List user's notes
POST            /notes                Yes       Create note

## How to Test Auth
1. Login:
curl -X POST http://127.0.0.1:5000/login
2. Use Token

## Project Structure
|- app.py
|- config.py (handles DATABASE_URL)
|- extensions.py (db, migrate, bcrypt, jwt)
|- models.py (User, Note)
|- auth.py (/register, /login, /protected)
|- notes.py (/notes CRUD)
|- seed.py
|- README.md