# notes-tracker

A Flask REST API for private notes. Users register and log in to receive a JWT; every notes request is limited to the authenticated user's own records.

## Setup

From the `app` directory:

```bash
pipenv install
pipenv shell
export FLASK_APP=app.py
flask db upgrade
python seed.py
```

This repository includes the initial `migrations/` directory. If you are starting a new project without it, generate it once with `flask db init` followed by `flask db migrate -m "Create users and notes tables"` before running `flask db upgrade`.

For a non-development environment, set a long, random `JWT_SECRET_KEY` before starting the app. The development database is SQLite at `notes_tracker.db`.

## Run

```bash
flask run
```

The API runs at `http://127.0.0.1:5000` by default. Seeded accounts are `alice` and `bob`, both with password `password123`.

## Endpoints

All error responses use `{"error": "message"}`. Notes routes require `Authorization: Bearer <access_token>` and return `401` when the token is missing, invalid, or expired. A note belonging to another user returns `404` to avoid revealing its existence.

### Register — `POST /register` (public)

Request:

```json
{"username":"jane","email":"jane@example.com","password":"password123"}
```

Response `201`:

```json
{"user":{"id":3,"username":"jane","email":"jane@example.com"}}
```

### Login — `POST /login` (public)

Request:

```json
{"username":"alice","password":"password123"}
```

Response `200`:

```json
{"access_token":"<jwt>","user":{"id":1,"username":"alice","email":"alice@example.com"}}
```

### Current user — `GET /me` (JWT required)

Response `200`:

```json
{"user":{"id":1,"username":"alice","email":"alice@example.com"}}
```

### List notes — `GET /notes?page=1&per_page=10` (JWT required)

Response `200`:

```json
{"notes":[{"id":1,"title":"Welcome","content":"This is Alice's first note.","created_at":"2026-01-01T00:00:00+00:00","user_id":1}],"pagination":{"total":3,"page":1,"pages":1}}
```

### Get one note — `GET /notes/<id>` (JWT required)

Response `200`: a `note` object in the same shape as the create-note response. A missing or another user's note returns `404`.

### Create note — `POST /notes` (JWT required)

Request:

```json
{"title":"Today","content":"Finish the API documentation."}
```

Response `201`:

```json
{"note":{"id":7,"title":"Today","content":"Finish the API documentation.","created_at":"2026-01-01T00:00:00+00:00","user_id":1}}
```

### Update note — `PATCH /notes/<id>` (JWT required)

Request:

```json
{"title":"Updated title","content":"Updated content."}
```

Response `200`: the updated `note` object in the same shape as create. Supply either `title`, `content`, or both.

### Delete note — `DELETE /notes/<id>` (JWT required)

Response `204` with an empty body.

## Status codes

`200` successful login/read/update; `201` created; `204` deleted; `400` invalid input; `401` missing or invalid JWT (or invalid login); `404` unknown route or inaccessible/missing note.
