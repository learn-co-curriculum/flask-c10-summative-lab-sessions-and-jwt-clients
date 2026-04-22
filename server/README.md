# Notes App - Flask API Backend

## Description
A secure RESTful API backend for a personal Notes application built with Flask.
Users can register, log in, and manage their own private notes.
No user can view, create, edit, or delete another user's notes.

## Tech Stack
- Python 3.8.13+
- Flask 2.2.2
- Flask-SQLAlchemy 3.0.3
- Flask-Migrate 4.0.0
- Flask-RESTful 0.3.9
- Flask-Bcrypt 1.0.1
- SQLite (development database)

## Project Structure
server/
├── app.py              # App entry point, route registration
├── config.py           # App factory, extensions, configuration
├── models.py           # User and Note database models
├── seed.py             # Database seeding script
├── README.md           # Project documentation
└── resources/
├── init.py
├── auth.py         # Register, Login, Logout, CheckSession
└── notes.py        # Notes CRUD endpoints

## Installation

### 1. Clone the repository
```bash
git clone <your-repo-url>
cd summative-lab-with-client-apps/server
```

### 2. Install dependencies
```bash
pipenv install
pipenv shell
```

### 3. Set up the database
```bash
flask db init
flask db migrate -m "Initial migration"
flask db upgrade
```

### 4. Seed the database
```bash
python seed.py
```

### 5. Run the server
```bash
python app.py
```

The API will be running at `http://localhost:5555`

## API Endpoints

### Auth
| Method | Endpoint | Description |
|--------|-------------|-------------|
| POST | /register | Create a new user account |
| POST | /login | Log in to existing account |
| DELETE | /logout | Log out current user |
| GET | /check_session | Check if user is logged in |

### Notes
| Method | Endpoint | Description |
|--------|-------------|-------------|
| GET | /notes | Get all notes (paginated) |
| POST | /notes | Create a new note |
| GET | /notes/<id> | Get a single note |
| PATCH | /notes/<id> | Update a note |
| DELETE | /notes/<id> | Delete a note |

## Pagination
The `GET /notes` endpoint supports pagination via query parameters:
- `page` — page number (default: 1)
- `per_page` — results per page (default: 5)

Example: `GET /notes?page=2&per_page=10`

## Test User Credentials
After seeding, you can log in with:
- **Username:** testuser
- **Password:** password123

## Security
- Passwords are hashed using Flask-Bcrypt
- Sessions are used for authentication
- All notes endpoints require authentication
- Users can only access their own notes