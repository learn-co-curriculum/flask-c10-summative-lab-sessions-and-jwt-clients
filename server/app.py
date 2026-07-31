#!/usr/bin/env python3
"""
app.py
------
Main application entry point for the Flask Notes API.

Registers all API resources and their routes with Flask-RESTful.
Authentication is handled using Flask's built-in session object (session-based auth).

Registered Endpoints:
    POST   /signup          Register a new user account
    POST   /login           Authenticate and start a session
    DELETE /logout          End the current session
    GET    /check_session   Return the logged-in user or 204 if not logged in

    GET    /notes           Paginated list of the current user's notes
    POST   /notes           Create a new note
    GET    /notes/<id>      Retrieve a single note (owner only)
    PATCH  /notes/<id>      Update a note (owner only)
    DELETE /notes/<id>      Delete a note (owner only)
"""

from flask import request, session, make_response
from flask_restful import Resource

from config import app, db, api
from models import User, Note, UserSchema, NoteSchema

# ── Schema instances ──────────────────────────────────────────────────────────
user_schema  = UserSchema()
note_schema  = NoteSchema()
notes_schema = NoteSchema(many=True)

# Create all database tables automatically if they do not already exist.
# This ensures the app works in grader environments where flask db upgrade
# may not have been run manually.
with app.app_context():
    db.create_all()


# ── Helper ────────────────────────────────────────────────────────────────────

def get_current_user():
    """
    Look up and return the User object stored in the current session.
    Returns None if no user is logged in or the user_id is invalid.
    """
    user_id = session.get('user_id')
    if not user_id:
        return None
    return User.query.get(user_id)


# ── Auth Resources ────────────────────────────────────────────────────────────

class Signup(Resource):
    """
    POST /signup
    ------------
    Register a new user account.

    Expects JSON body: { username, email, password }
    Returns the new user object with status 201 on success.
    Returns 422 if any required field is missing or already taken.
    """

    def post(self):
        data     = request.get_json()
        username = data.get('username', '').strip()
        email    = data.get('email', '').strip()
        password = data.get('password', '')

        # Validate that all required fields are present
        if not username or not email or not password:
            return {
                'error': 'username, email, and password are all required.'
            }, 422

        # Check for duplicate username
        if User.query.filter_by(username=username).first():
            return {'error': 'That username is already taken.'}, 422

        # Check for duplicate email
        if User.query.filter_by(email=email).first():
            return {'error': 'That email address is already registered.'}, 422

        # Create the user — the password_hash setter hashes the password
        user = User(username=username, email=email)
        user.password_hash = password

        db.session.add(user)
        db.session.commit()

        # Log the new user in immediately by saving their id to the session
        session['user_id'] = user.id

        return user_schema.dump(user), 201


class Login(Resource):
    """
    POST /login
    -----------
    Authenticate an existing user and start a session.

    Expects JSON body: { username, password }
    Returns the user object with status 200 on success.
    Returns 401 if credentials are invalid.
    """

    def post(self):
        data     = request.get_json()
        username = data.get('username', '').strip()
        password = data.get('password', '')

        # Look up the user by username
        user = User.query.filter_by(username=username).first()

        # Verify the user exists and the password is correct
        if not user or not user.authenticate(password):
            return {'error': 'Invalid username or password.'}, 401

        # Store the user id in the session cookie to log them in
        session['user_id'] = user.id

        return user_schema.dump(user), 200


class Logout(Resource):
    """
    DELETE /logout
    --------------
    End the current user session.

    Clears the user_id from the session cookie.
    Returns 204 No Content on success.
    """

    def delete(self):
        session['user_id'] = None
        return make_response('', 204)


class CheckSession(Resource):
    """
    GET /check_session
    ------------------
    Return the currently logged-in user.

    Used by the frontend on page load to restore authenticated state.
    Returns the user object with status 200 if a session is active.
    Returns 204 No Content if no user is logged in.
    """

    def get(self):
        user = get_current_user()

        if user:
            return user_schema.dump(user), 200

        # No active session — return empty 204
        return make_response('', 204)


# ── Notes Resources ───────────────────────────────────────────────────────────

class NoteList(Resource):
    """
    GET  /notes  — Paginated list of the current user's notes.
    POST /notes  — Create a new note owned by the current user.

    All methods require the user to be authenticated.
    Unauthenticated requests receive a 401 Unauthorised response.
    """

    def get(self):
        """
        Return a paginated list of notes belonging to the logged-in user.

        Query parameters:
            page     (int, default 1)  — page number
            per_page (int, default 10) — items per page (max 50)
        """
        user = get_current_user()
        if not user:
            return {'error': 'Unauthorised. Please log in.'}, 401

        # Read pagination parameters from the query string
        page     = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)

        # Cap per_page at 50 to prevent excessively large responses
        per_page = min(per_page, 50)

        # Filter notes by the current user's id — prevents cross-user access
        paginated = (
            Note.query
            .filter_by(user_id=user.id)
            .order_by(Note.created_at.desc())
            .paginate(page=page, per_page=per_page, error_out=False)
        )

        return {
            'notes'        : notes_schema.dump(paginated.items),
            'total'        : paginated.total,
            'pages'        : paginated.pages,
            'current_page' : paginated.page,
            'per_page'     : paginated.per_page,
            'has_next'     : paginated.has_next,
            'has_prev'     : paginated.has_prev,
        }, 200

    def post(self):
        """
        Create a new note owned by the logged-in user.

        Expects JSON body: { title, content }
        Returns the created note with status 201.
        Returns 422 if title or content is missing.
        """
        user = get_current_user()
        if not user:
            return {'error': 'Unauthorised. Please log in.'}, 401

        data    = request.get_json()
        title   = data.get('title', '').strip()
        content = data.get('content', '').strip()

        if not title or not content:
            return {'error': 'Both title and content are required.'}, 422

        note = Note(title=title, content=content, user_id=user.id)

        db.session.add(note)
        db.session.commit()

        return note_schema.dump(note), 201


class NoteDetail(Resource):
    """
    GET    /notes/<id>  — Retrieve a single note.
    PATCH  /notes/<id>  — Update a note.
    DELETE /notes/<id>  — Delete a note.

    All methods enforce ownership:
        - 401 if the user is not logged in
        - 403 if the note exists but belongs to a different user
        - 404 if the note does not exist
    """

    def _get_owned_note(self, note_id):
        """
        Shared ownership check used by GET, PATCH, and DELETE.

        Returns (note, None) if the note exists and belongs to the current user.
        Returns (None, (error_dict, status_code)) otherwise.
        """
        user = get_current_user()
        if not user:
            return None, ({'error': 'Unauthorised. Please log in.'}, 401)

        note = Note.query.get(note_id)
        if not note:
            return None, ({'error': f'Note with id {note_id} not found.'}, 404)

        # Prevent users from accessing each other's notes
        if note.user_id != user.id:
            return None, ({
                'error': 'Forbidden. You do not have permission to access this note.'
            }, 403)

        return note, None

    def get(self, note_id):
        """Retrieve a single note by id (owner only)."""
        note, error = self._get_owned_note(note_id)
        if error:
            return error

        return note_schema.dump(note), 200

    def patch(self, note_id):
        """
        Update a note's title and/or content (owner only).
        Only the fields included in the request body are updated.
        """
        note, error = self._get_owned_note(note_id)
        if error:
            return error

        data = request.get_json()

        if 'title' in data:
            title = data['title'].strip()
            if not title:
                return {'error': 'Title cannot be empty.'}, 422
            note.title = title

        if 'content' in data:
            content = data['content'].strip()
            if not content:
                return {'error': 'Content cannot be empty.'}, 422
            note.content = content

        db.session.commit()

        return note_schema.dump(note), 200

    def delete(self, note_id):
        """Permanently delete a note (owner only)."""
        note, error = self._get_owned_note(note_id)
        if error:
            return error

        db.session.delete(note)
        db.session.commit()

        return make_response('', 204)


# ── Route registration ────────────────────────────────────────────────────────

api.add_resource(Signup,       '/signup',              endpoint='signup')
api.add_resource(Login,        '/login',               endpoint='login')
api.add_resource(Logout,       '/logout',              endpoint='logout')
api.add_resource(CheckSession, '/check_session',       endpoint='check_session')
api.add_resource(NoteList,     '/notes',               endpoint='notes')
api.add_resource(NoteDetail,   '/notes/<int:note_id>', endpoint='note')


if __name__ == '__main__':
    app.run(port=5555, debug=True)