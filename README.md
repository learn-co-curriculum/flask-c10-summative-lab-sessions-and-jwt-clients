# TaskFlow API

TaskFlow is a simple productivity application backend built using Flask. It allows users to create accounts, log in, and manage their own tasks.

This project was developed as part of my Flask summative assessment to practice authentication, database relationships, REST APIs, and CRUD operations.

## Technologies Used

- Python
- Flask
- Flask-SQLAlchemy
- Flask-Migrate
- Flask-Bcrypt
- SQLite
- Pipenv

## Features

- User registration and login
- Password hashing
- Session-based authentication
- User logout
- Create, view, update, and delete tasks
- Task ownership: users can only access their own tasks
- Task pagination
- Sample database records using a seed file

## Database Models

### User
- id
- username
- password_hash

### Task
- id
- title
- description
- completed
- user_id

A user can have many tasks, but each task belongs to one user.

## Installation

Clone the repository:

```bash
git clone https://github.com/khishaplays/flask-c10-summative-lab-sessions-and-jwt-clients.git
cd flask-c10-summative-lab-sessions-and-jwt-clients
```

Switch to the backend development branch:

```bash
git checkout feature/flask-backend
```

Open the server directory and install dependencies:

```bash
cd server
pipenv install
pipenv shell
```

## Database Setup

Apply the database migrations:

```bash
flask --app app db upgrade
```

Add sample records:

```bash
python seed.py
```

## Running the Server

```bash
python app.py
```

The API runs at:

http://127.0.0.1:5000

## API Endpoints

### Authentication

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | /signup | Register a user |
| POST | /login | Log in |
| GET | /check_session | Check the current user |
| DELETE | /logout | Log out |

### Tasks

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | /tasks | View your tasks |
| POST | /tasks | Create a task |
| GET | /tasks/<id> | View one task |
| PATCH | /tasks/<id> | Update a task |
| DELETE | /tasks/<id> | Delete a task |

## Pagination

Tasks are displayed in pages of five.

Example:

```text
GET /tasks?page=1
GET /tasks?page=2
```

The response includes the tasks, current page, total number of tasks, and number of pages.

## Testing

I tested the API using curl commands in the terminal.

The tests covered:
- User registration and login
- Session checking and logout
- Creating tasks
- Viewing tasks
- Updating tasks
- Deleting tasks
- Pagination
- Unauthorized requests

## What I Learned

This project helped me understand how Flask handles HTTP requests, how SQLAlchemy connects models to a database, and how session authentication protects user data.

I also practiced organizing a backend project, using database migrations, and testing API endpoints.

## Author

Khisha
