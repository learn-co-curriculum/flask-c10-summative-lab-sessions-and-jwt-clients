# Flask JWT Lab Sessions and Clients

This project consists of a Flask backend with JWT authentication and a React frontend client.

## Backend Setup

1. Navigate to the `server` directory:
   ```bash
   cd server
   ```

2. Install dependencies:
   ```bash
   pipenv install
   ```

3. Run the database seed:
   ```bash
   pipenv run python seed.py
   ```

4. Start the server:
   ```bash
   pipenv run python run.py
   ```
   The server runs on `http://localhost:5555`.

## Frontend Setup

1. Navigate to the `client-with-jwt` directory:
   ```bash
   cd client-with-jwt
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Start the development server:
   ```bash
   npm start
   ```
   The frontend runs on `http://localhost:4000` and proxies API calls to the backend.

## Testing with Postman

1. Start the backend server as described above.

2. Open Postman and create a new collection.

### Authentication Endpoints

#### Signup
- **Method**: POST
- **URL**: `http://localhost:5555/signup`
- **Headers**:
  - `Content-Type: application/json`
- **Body** (raw JSON):
  ```json
  {
    "username": "testuser",
    "password": "password123",
    "password_confirmation": "password123"
  }
  ```
- **Expected Response**: 201 Created with token and user data.

#### Login
- **Method**: POST
- **URL**: `http://localhost:5555/login`
- **Headers**:
  - `Content-Type: application/json`
- **Body** (raw JSON):
  ```json
  {
    "username": "alice@example.com",
    "password": "password123"
  }
  ```
- **Expected Response**: 200 OK with token and user data.
- **Note**: Save the token from the response for authenticated requests.

#### Get Current User
- **Method**: GET
- **URL**: `http://localhost:5555/me`
- **Headers**:
  - `Authorization: Bearer <token>`
- **Expected Response**: 200 OK with user data.

### Notes Endpoints

#### Get Notes
- **Method**: GET
- **URL**: `http://localhost:5555/notes`
- **Headers**:
  - `Authorization: Bearer <token>`
- **Expected Response**: 200 OK with array of notes.

#### Create Note
- **Method**: POST
- **URL**: `http://localhost:5555/notes`
- **Headers**:
  - `Content-Type: application/json`
  - `Authorization: Bearer <token>`
- **Body** (raw JSON):
  ```json
  {
    "title": "My Note",
    "content": "This is a test note."
  }
  ```
- **Expected Response**: 201 Created with note data.

#### Update Note
- **Method**: PATCH
- **URL**: `http://localhost:5555/notes/<note_id>`
- **Headers**:
  - `Content-Type: application/json`
  - `Authorization: Bearer <token>`
- **Body** (raw JSON):
  ```json
  {
    "title": "Updated Title",
    "content": "Updated content."
  }
  ```
- **Expected Response**: 200 OK with updated note data.

#### Delete Note
- **Method**: DELETE
- **URL**: `http://localhost:5555/notes/<note_id>`
- **Headers**:
  - `Authorization: Bearer <token>`
- **Expected Response**: 204 No Content.

### Tags Endpoints

Similar to Notes, replace `/notes` with `/tags` and use appropriate fields (name, color).

## Running Tests

To run the backend tests:
```bash
cd server
pipenv run pytest
```

## Sample Users

- Username: `alice@example.com`, Password: `password123`
- Username: `bob@example.com`, Password: `password123`
