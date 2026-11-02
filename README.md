# Personal Notes API

## Project Description

Personal Notes API is a Flask backend for a personal notes application.

Users can create accounts, log in, and manage their personal notes. Each user should only be able to access, update, and delete their own notes.

This project uses session-based authentication and is developed by a five-member Moringa group.

The provided React frontend in `client-with-sessions` handles signup and login. Notes endpoints can be tested using Postman or curl.

## Technologies

* Python
* Flask
* Flask-SQLAlchemy
* SQLite
* Flask-Migrate
* Flask-Bcrypt
* Flask Sessions
* React
* Git and GitHub

## Project Structure

```text
project-root/
├── client-with-jwt/
├── client-with-sessions/
├── server/
│   ├── app.py
│   ├── config.py
│   ├── models.py
│   ├── seed.py
│   ├── requirements.txt
│   └── routes/
│       ├── auth.py
│       └── notes.py
├── README.md
├── TESTING.md
└── .gitignore

```

## Backend Setup

1. Clone the repository:

```bash
git clone https://github.com/ManwaMocha/flask-c10-summative-lab-sessions-and-jwt-clients.git
```

2. Navigate into the server directory:

```bash
cd flask-c10-summative-lab-sessions-and-jwt-clients
cd server
```

3. Create a virtual environment:

```bash
python3 -m venv venv
```

4. Activate the virtual environment:

```bash
source venv/bin/activate
```

5. Install dependencies:

```bash
pip install -r requirements.txt
```

## Running the Backend

From inside the `server` directory, run:

```bash
python -m flask --app app run --port 5555 --debug
```

The backend will be available at:

`http://127.0.0.1:5555`

## Authentication

The application uses session-based authentication.

Users must log in before accessing protected notes functionality. Each user should only be able to manage their own notes.

## Testing

API endpoints can be tested using Postman or curl.

See `TESTING.md` for the manual testing instructions and expected API behaviour.

## Contributors

This project was developed collaboratively by a five-member Moringa School group.
