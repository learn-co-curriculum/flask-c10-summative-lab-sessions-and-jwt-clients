# Workout Tracker API
## Project Description
- This Workout Tracker API is a secure RESTful Flask backend that allows users to register, log in, and manage their personal workouts.
- Authentication is implemented using **Session-Based Authentication**, ensuring that only authenticated users can access protected routes. 
- Each user has their own collection of workouts through a **one-to-many relationship**, and users can only view, update, or delete workouts that belong to them.
- The API also supports pagination for retrieving workout records efficiently.

## Features
 - User registration with secure password hashing.
 - User login using session-based authentication.
 - Persistent login with session checking.
 - User logout.
 - One-to-many relationship between Users and Workouts.
 - Full CRUD operations for workouts.
 - Pagination for Workout listings.
 - Routes protection using @app.before_request.
 - Database migrations using Flask-Migrate.
 - Seed file with sample users and workouts generated using Faker.

 ## Technologies Used
    * Python3
    * Flask
    * Flask-RESTful
    * Flask-Migrate
    * Flask-Bcrypt
    * Marshmallow
    * SQLite
    * Faker
## Installation Instructions
1. Clone my github repository:
    ([[https://github.com/Celline-SD17/flask-c10-summative-lab-sessions-and-jwt-clients]])
2. Change directory to the cloned repo
3. Install project dependencies
    - pipenv install
    - pipenv shell
4. Initialize migrations for the first time only
    - flask db init
5. Generate a migration
    - flask db migrate -m "Initial migration"
6. Apply the migration
    - flask db upgrade
7. Seed the database
    -python3 seed.py
## Run Instructions
- From the **server** directory, start the Flask server through the command:
    * flask run
- The API will run on:
    ([[http://127.0.0.1:5555]])
- If using the provided React frontend, start it from the client directory:
    * npm install
    * npm run
## API Endpoints
```
**Method**        **Endpoint**                  **Description**
POST              /signup                   Register a new user account.
POST              /login                    Authenticate a user and begin a session. 
GET               /check_session            Returns the currently logged-in user if authenticated.
DELETE            /logout                   Ends the current user session.
GET               /workouts                 Returns the authenticated user's workouts with pagination support.
POST              /workouts                 Creates a new workout for the authenticated user. 
GET               /workouts/<id>            Retrieves a single workout owned by the authenticated user.
PATCH             /workouts/<id>            Updates a workout owned by the authenticated user.
DELETE            /workouts/<id>            Deletes a workout owned by the authenticated user     
```

## Pagination
- The GET /workouts endpoint supports pagination using query parameters
### Query Parameters
```
Parameter	         Description	                                  Default
page	        Specifies which page of results to return.	            1
per_page	    Specifies the number of workouts returned per page.	    3
```

**Example Requests**
- To retrieve the first page of workouts, use :
    * GET /workouts?page=1
- Retrieve the second page of workouts:
    * GET /workouts?page=2
- Retrieve two workouts per page:
    * GET /workouts?page=1&per_page=2
- Pagination only returns workouts that belong to the authenticated user. 

## Security
- The API protects all private routes through the `@app.before_request`
- Public access is limited to authentication endpoints, while all workout routes require a valid user session.
- Users are authorized to access only their own workout records. 

## Authentication
- This project uses **session-based authentication**
- After a successful login
    * A session is created for the authenticated user.
    * Protected routes verify the session before processing requests.
    * Users can only access and modify workouts that belong to their own account.
- Passwords are securely stored using FLASK-Bcrypt and are never saved as plain text.

## Database Structure
### User
    * id
    * username
    * password_hash
### Workout
    * id
    * title
    * duration
    * date
    * user_id
### Relationship
    * One User can have many Workouts.
    * Each Workout belongs to one User.

## Author
- Developed as a Flask authentication and authorization backend project demonstrating secure user authentication, protected RESTful routes, one-to-many relationships, and pagination. 






