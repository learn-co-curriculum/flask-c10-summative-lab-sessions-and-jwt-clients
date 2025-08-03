# Flask JWT Notes API

A secure Flask API for user registration, login, and personal notes management. Each user can only access their own notes.

## Table of Contents

1. [Installation](#installation)
2. [Running](#running)
3. [Endpoints](#endpoints)
4. [Auth Endpoints Response Format](#auth-endpoints-response-format)
5. [Example `curl` Commands](#example-curl-commands)

## Installation

1. **Clone the repo**

    ```bash
    git clone https://github.com/tlgrf/flask-c10-summative-lab-sessions-and-jwt-clients
    cd flask-c10-summative-lab-sessions-and-jwt-clients
    ```

2. **Install dependencies**

    ```bash
    pipenv install
    pipenv install "werkzeug<2.3"
    ```

3. **Set up the database**

    ```bash
    pipenv shell
    export FLASK_APP=app.py
    flask db init 
    flask db migrate -m "Initial migration"
    flask db upgrade
    ```

4. **Seed the database**

    ```bash
    python seed.py
    ```

## Running

```bash
flask run
```

---

## Endpoints

- `POST /signup` – Register new user
- `POST /login` – Login and get JWT
- `GET /me` – Get current user info (JWT required)
- `GET /notes` – List notes (JWT required, paginated)
- `POST /notes` – Create note (JWT required)
- `PATCH /notes/<id>` – Update note (JWT required)
- `DELETE /notes/<id>` – Delete note (JWT required)

---

## Auth Endpoints Response Format

**POST /signup** and **POST /login**:

```json
{
  "token": "<JWT string>",
  "user": {
    "id": 1,
    "username": "string"
  }
}
```

**GET /me**:

```json
{
  "id": 1,
  "username": "string"
}
```

---

## Example `curl` Commands

**Sign up:**

```sh
curl -X POST http://127.0.0.1:5000/signup \
  -H "Content-Type: application/json" \
  -d '{"username": "yourname", "password": "yourpassword"}'
```

**Login:**

```sh
curl -X POST http://127.0.0.1:5000/login \
  -H "Content-Type: application/json" \
  -d '{"username": "yourname", "password": "yourpassword"}'
```

**Get notes:**

```sh
curl -X GET http://127.0.0.1:5000/notes \
  -H "Authorization: Bearer YOUR_TOKEN_HERE"
```
