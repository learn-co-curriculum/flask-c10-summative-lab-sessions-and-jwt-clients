# Student 2: Authentication — ibraanwar7565-ai

This feature adds session authentication to the existing personal reading tracker backend. It preserves the User and ReadingEntry models and migration history. No JWT authentication is used.

## Run locally

From the repository root, using Python 3.10–3.12:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
$env:SECRET_KEY = python -c "import secrets; print(secrets.token_hex(32))"
cd Personal-reading-tracker
python -m flask --app app db upgrade
python seed.py
python app.py
```

Keep the same secret between restarts if existing sessions should remain valid. Never commit it. On macOS/Linux, activate with `source .venv/bin/activate` and set the secret with `export SECRET_KEY=$(python -c 'import secrets; print(secrets.token_hex(32))')`.

The API runs on port 5555. Seed credentials: `jamesk` / `password123` and `aisha_m` / `password123`. Seeding clears existing users and reading entries; use it only for development.

## Endpoints

| Method | Path | Result |
| --- | --- | --- |
| POST | /register | Create user and start session; 201 |
| POST | /signup | Alias for /register; 201 |
| POST | /login | Authenticate and start session; 200 |
| GET | /check_session | Current public user; 200 or 401 |
| DELETE | /logout | Clear browser session; 204 or 401 |

Registration JSON:

```json
{"username":"ibraanwar","email":"ibraanwar@example.com","password":"password123","password_confirmation":"password123"}
```

Confirmation is optional, but must match when supplied. Username accepts 3–80 letters, digits, underscores or hyphens. Passwords require at least 8 characters and at most 72 UTF-8 bytes, the bcrypt input limit. Email is required by the existing database model and is normalized to lowercase. Duplicate usernames/emails and invalid input return 400. Unknown fields are rejected.

Login JSON:

```json
{"username":"ibraanwar","password":"password123"}
```

Responses contain only `id`, `username`, and `email`. Passwords and hashes never appear in API responses. Errors use `{"errors":["message"]}` to match the supplied client's error handling. In Postman, retain the session cookie across requests.

## Student 3 integration

All registered endpoints except signup, registration, login, static files and OPTIONS require a valid session by default. Import and register resource routes in `create_app` before returning the app. Existing direct `@app.route` definitions can also be placed after `app = create_app()`.

The reusable decorator and authenticated user are available as:

```python
from auth import login_required
from flask import g

@app.get('/reading_entries')
@login_required
def index():
    entries = ReadingEntry.query.filter_by(user_id=g.current_user.id)
    # Apply pagination and serialize using the team's resource schema.
```

For create, always assign `user_id=g.current_user.id`; never trust a client-supplied owner. For get/update/delete, query by both resource ID and `g.current_user.id`. Authentication alone does not enforce ownership. Student 3 must implement and test ownership and pagination; this branch does not add CRUD endpoints.

Auth schemas live in `auth_schemas.py` so Student 4 can keep working in `schemas.py` without a filename conflict.

## Frontend and security configuration

Use `client-with-sessions`. Its login, check-session and logout contracts match this API. Its original signup form sends no email, while the teammate's User model requires email. Add an email input to that form and include it in the signup JSON for browser registration; until then, registration can be tested through Postman. No frontend files were changed for this backend assignment.

Cookies are HttpOnly and SameSite=Lax, and sessions expire after 8 hours without sliding renewal. Set `COOKIE_SECURE=true` for HTTPS deployment. Set `TRUSTED_ORIGINS` to a comma-separated list of exact allowed frontend origins (defaults: http://localhost:4000,http://localhost:5555). Write requests from other browser origins are rejected; POST/PATCH/PUT require JSON. Serve frontend and API through the same origin/proxy; do not add permissive credentialed CORS.

Flask uses signed cookies: logout removes the browser cookie, but a previously copied cookie remains usable until expiration. Immediate server-side revocation would require server-side session storage. Use HTTPS and keep SECRET_KEY private.

## Verification

From the repository root:

```powershell
python -m pytest Personal-reading-tracker/tests -q
```

22 automated tests pass: registration and bcrypt storage, login, logout, public serialization, duplicate and invalid input, JSON validation, password byte limits, protected HTTP methods, two independent users, deleted users, origin checks, signup alias, and required secret configuration. The existing pinned pytest/Werkzeug versions emit Python 3.12 deprecation warnings.

This is the Student 2 contribution. The complete group project still requires Student 3's CRUD/ownership/pagination and Student 4's resource schemas and final documentation to be integrated and tested.
