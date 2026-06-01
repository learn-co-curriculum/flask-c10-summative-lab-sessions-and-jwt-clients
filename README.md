# Flask Auth + Notes API (JWT Backend)

## Project Overview

This project is a Flask backend API for a simple productivity tool. It includes user authentication (signup/login with JWT) and a protected Notes system where users can create, read, update, and delete their own notes.

---

##  Features

### Authentication

* User Signup
* User Login (returns JWT token)
* Get Current User (`/me`) using token
* Passwords securely hashed using Bcrypt

### Notes System (Protected Routes)

* Create a note
* Get all notes (user-specific)
* Get single note
* Update note
* Delete note
* Optional filtering by category

### Security

* JWT authentication protects all notes routes
* Users can only access their own notes

---

##  Tech Stack

* Python
* Flask
* Flask-SQLAlchemy
* Flask-Migrate (Alembic)
* Flask-Bcrypt
* Flask-JWT-Extended
* SQLite

---

##  Installation & Setup

### 1. Clone the project

```bash
git clone <repo-url>
cd flask-c10-summative-lab-sessions-and-jwt-clients/server
```

### 2. Create virtual environment

```bash
pipenv install
pipenv shell
```

### 3. Install dependencies (if needed)

```bash
pip install flask flask-sqlalchemy flask-migrate flask-bcrypt flask-jwt-extended
```

### 4. Set up database

```bash
flask db init
flask db migrate -m "initial"
flask db upgrade
```

### 5. Run server

```bash
flask run
```

Server runs at:

```
http://127.0.0.1:5555
```

---

## Authentication Flow (Testing Guide)

### 1. Signup

`POST /signup`

```json
{
  "username": "john",
  "password": "1234"
}
```

Returns:

* JWT token
* User object

---

### 2. Login

`POST /login`

```json
{
  "username": "john",
  "password": "1234"
}
```

Returns:

JWT token

---

### 3. Get Current User

`GET /me`

Headers:

```
Authorization: Bearer <your_token>
```

---

## Notes API (Protected)

All requests require:

```
Authorization: Bearer <token>
```

---

### Create Note

`POST /notes`

```json
{
  "title": "Test",
  "content": "Hello world",
  "category": "work"
}
```

---

### Get All Notes

`GET /notes`

Optional filter:

```
/notes?category=work
```

---

### Get Single Note

`GET /notes/<id>`

---

### Update Note

`PATCH /notes/<id>`

```json
{
  "title": "Updated title"
}
```

---

### Delete Note

`DELETE /notes/<id>`

---

## 🧪 Seed Data (Optional)

If a seed file is included:

```bash
python seed.py
```

---

## Project Structure

```
server/
│
├── app.py
├── config.py
├── models.py
├── routes/
│   ├── auth.py
│   └── notes.py
├── migrations/
└── instance/
    └── app.db
```

---

## 👨‍💻 Author

Built as a Flask JWT authentication + CRUD lab project.
