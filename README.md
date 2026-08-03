# Secure Notes API

Session-authenticated Flask API backing the provided `client-with-sessions` frontend. Notes always belong to the logged-in user; every resource query filters by `session['user_id']`.

## Setup

```powershell
pipenv install
pipenv run flask --app app db upgrade
pipenv run python seed.py
pipenv run python app.py
```

The API runs at `http://localhost:5555`. Set a strong `SECRET_KEY` (and `SESSION_COOKIE_SECURE=true` when using HTTPS) outside development.

## Endpoints

| Method | Endpoint | Purpose |
| --- | --- | --- |
| POST | `/signup` | Create account and log in |
| POST | `/login` | Log in |
| GET | `/check_session` | Return current user or `{}` |
| DELETE | `/logout` | End session |
| GET | `/notes?page=1&per_page=10` | Paginated current user's notes |
| POST | `/notes` | Create a note (`title`, `content`) |
| GET | `/notes/:id` | Read an owned note |
| PATCH | `/notes/:id` | Update an owned note |
| DELETE | `/notes/:id` | Delete an owned note |

Resource endpoints require authentication. Requests for another user's note receive `404`, preventing record discovery. The index response contains `notes`, `page`, `per_page`, `total`, and `pages`.
