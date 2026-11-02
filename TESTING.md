# Personal Notes API – Testing Guide

## 1. Introduction

This document explains how to manually test the Personal Notes API using Postman or curl.

The API allows users to register, log in, create notes, view notes, update notes and delete notes.

## 2. Starting the Backend

Navigate to the server directory:

```bash
cd server
```

Activate the virtual environment:

```bash
source venv/bin/activate
```

Start the Flask application:

```bash
python app.py
```

The backend runs at:

`http://127.0.0.1:5555`

## 3. Notes API Endpoints

All notes endpoints require an authenticated session.

| Method | Endpoint           | Description                 | Expected Status |
| ------ | ------------------ | --------------------------- | --------------- |
| GET    | `/notes`           | Retrieve all personal notes | 200             |
| GET    | `/notes/<note_id>` | Retrieve one note           | 200             |
| POST   | `/notes`           | Create a new note           | 201             |
| PATCH  | `/notes/<note_id>` | Update a note               | 200             |
| DELETE | `/notes/<note_id>` | Delete a note               | 204             |

## 4. Authentication Testing

Before testing protected notes endpoints:

1. Register a new user.
2. Log in using the registered credentials.
3. Maintain the session cookie when making subsequent requests.
4. Log out after completing the tests.

The exact authentication endpoint paths will be added after the authentication routes are integrated.

## 5. Creating a Note

**Request:**

POST `/notes`

Example JSON body:

```json
{
    "title": "My First Note",
    "content": "This is my first personal note."
}
```

Expected result: `201 Created`.

## 6. Retrieving Notes

**Retrieve all notes:**

GET `/notes`

Expected result: `200 OK`.

**Retrieve one note:**

GET `/notes/1`

Expected result: `200 OK` if the note belongs to the logged-in user.

## 7. Updating a Note

**Request:**

PATCH `/notes/1`

Example JSON body:

```json
{
    "title": "Updated Note",
    "content": "This is the updated content."
}
```

Expected result: `200 OK`.

## 8. Deleting a Note

**Request:**

DELETE `/notes/1`

Expected result: `204 No Content`.

## 9. Validation and Error Testing

| Test Case                                           | Expected Status                               |
| --------------------------------------------------- | --------------------------------------------- |
| Create note without a title                         | 400                                           |
| Create note with an empty title                     | 400                                           |
| Create note with a title longer than 150 characters | 400                                           |
| Create note without content                         | 400                                           |
| Update without title or content                     | 400                                           |
| Request a note that does not exist                  | 404                                           |
| Access notes without logging in                     | 401, subject to authentication implementation |
| Use invalid pagination values                       | 400                                           |

## 10. Authorization Testing

The following checks should be performed:

* A logged-in user should only retrieve their own notes.
* A user should not update another user's notes.
* A user should not delete another user's notes.
* A user should not access another user's private notes.

## 11. Session Testing

Test the following:

* Successful login creates an authenticated session.
* Protected endpoints reject unauthenticated requests.
* The session remains available across requests when cookies are maintained.
* Logging out ends the authenticated session.

## 12. Conclusion

Manual testing helps confirm that the API handles valid requests, invalid input, authentication and authorization correctly.
