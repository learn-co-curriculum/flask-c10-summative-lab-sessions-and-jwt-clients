# Running the app

Start the API on port 5555 (the port the frontend proxy expects):

bash
cd server
python app.py


In a second terminal, start the frontend:

bash
cd client-with-sessions
npm install
npm start


## Data models

- *User*: id, username (unique), hashed password.
- *Mood*: id, mood (one of happy, calm, excited, neutral, tired, sad, anxious, angry), intensity (1 to 10), note (optional), created_at, updated_at, user_id.
- *Journal*: id, title, content, created_at, updated_at, user_id.
- *Activity*: id, name (unique per user), user_id. Activities link to moods through a many-to-many relationship.

## Endpoints

All errors are returned as {"errors": ["message"]}. Every endpoint except signup, login and check_session requires a logged-in user, and returns 401 otherwise. Requesting another user's record returns 404.

### Authentication

| Method | Path | Description |
|---|---|---|
| POST | /signup | Create an account and log in. Body: username, password, password_confirmation. Returns 201 with the user, or 422 with errors. |
| POST | /login | Log in. Body: username, password. Returns 200 with the user, or 401. |
| GET | /check_session | Returns the logged-in user (200), or 401 if nobody is logged in. |
| DELETE | /logout | Log out. Returns 204. |

### Moods

| Method | Path | Description |
|---|---|---|
| GET | /moods?page=1&per_page=10 | Paginated list of the user's moods, newest first. |
| POST | /moods | Create a mood. Body: mood, intensity, optional note. Returns 201. |
| GET | /moods/<id> | One mood, including its activities. |
| PATCH | /moods/<id> | Update any of mood, intensity, note. |
| DELETE | /moods/<id> | Delete a mood. Returns 204. |
| POST | /moods/<mood_id>/activities/<activity_id> | Attach an activity to a mood. |
| DELETE | /moods/<mood_id>/activities/<activity_id> | Remove an activity from a mood. |

### Journals

| Method | Path | Description |
|---|---|---|
| GET | /journals?page=1&per_page=10 | Paginated list of the user's journal entries, newest first. |
| POST | /journals | Create an entry. Body: title, content. Returns 201. |
| GET | /journals/<id> | One journal entry. |
| PATCH | /journals/<id> | Update title and/or content. |
| DELETE | /journals/<id> | Delete an entry. Returns 204. |

### Activities

| Method | Path | Description |
|---|---|---|
| GET | /activities?page=1&per_page=10 | Paginated list of the user's activities, alphabetical. |
| POST | /activities | Create an activity. Body: name. Returns 201. |
| GET | /activities/<id> | One activity. |
| PATCH | /activities/<id> | Rename an activity. |
| DELETE | /activities/<id> | Delete an activity (it is also removed from any moods). Returns 204. |

### Paginated response format

json
{
  "items": [],
  "page": 1,
  "per_page": 10,
  "total": 15,
  "pages": 2
}


per_page is capped at 50.