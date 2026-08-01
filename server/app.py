#!/usr/bin/env python3
from flask import request, session, make_response
from flask_restful import Resource

from config import app, db, api
from models import User, Note, UserSchema, NoteSchema

# ── Schema instances ──────────────────────────────────────────────────────────
user_schema  = UserSchema()
note_schema  = NoteSchema()
notes_schema = NoteSchema(many=True)

# Create all tables automatically so the app works in all environments
with app.app_context():
    db.create_all()


# ── Helper ────────────────────────────────────────────────────────────────────

def get_current_user():
    user_id = session.get('user_id')
    if not user_id:
        return None
    return User.query.get(user_id)


# ── Auth Resources ────────────────────────────────────────────────────────────

class Signup(Resource):
    def post(self):
        data                  = request.get_json()
        username              = data.get('username', '').strip()
        password              = data.get('password', '')
        password_confirmation = data.get('password_confirmation', '')

        # Collect all validation errors before responding
        errors = []

        if not username:
            errors.append('Username is required.')

        if not password:
            errors.append('Password is required.')

        if password and password != password_confirmation:
            # Checked only when a password was provided to avoid duplicate messages
            errors.append('Password and password confirmation must match.')

        if username and User.query.filter_by(username=username).first():
            errors.append('That username is already taken.')

        # Return all errors at once so the frontend can display them together
        if errors:
            return {'errors': errors}, 422

        # Create user — the password_hash setter hashes the value automatically
        user = User(username=username)
        user.password_hash = password

        db.session.add(user)
        db.session.commit()

        # Log the new user in immediately
        session['user_id'] = user.id

        return user_schema.dump(user), 201


class Login(Resource):
    def post(self):
        data     = request.get_json()
        username = data.get('username', '').strip()
        password = data.get('password', '')

        user = User.query.filter_by(username=username).first()

        # Fail with a single generic message to avoid exposing which field was wrong
        if not user or not user.authenticate(password):
            return {'errors': ['Invalid username or password.']}, 401

        session['user_id'] = user.id

        return user_schema.dump(user), 200


class Logout(Resource):
    def delete(self):
        session['user_id'] = None
        return {}, 204


class CheckSession(Resource):
    def get(self):
        user = get_current_user()

        if user:
            # r.ok = true → frontend calls r.json() → sets user state
            return user_schema.dump(user), 200

        # r.ok = false → frontend skips r.json() → user stays null → Login shown
        return {'errors': ['Not authenticated.']}, 401


# ── Notes Resources ───────────────────────────────────────────────────────────

class NoteList(Resource):
    def get(self):
        user = get_current_user()
        if not user:
            return {'errors': ['Unauthorised. Please log in.']}, 401

        page     = request.args.get('page', 1, type=int)
        per_page = min(request.args.get('per_page', 10, type=int), 50)

        # filter_by(user_id=user.id) ensures cross-user access is impossible
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
        user = get_current_user()
        if not user:
            return {'errors': ['Unauthorised. Please log in.']}, 401

        data    = request.get_json()
        title   = data.get('title', '').strip()
        content = data.get('content', '').strip()
        category = data.get('category', 'General').strip()note = Note(title=title, content=content,
            category=category, user_id=user.id)

        errors = []
        if not title:
            errors.append('Title is required.')
        if not content:
            errors.append('Content is required.')
        if errors:
            return {'errors': errors}, 422

        note = Note(title=title, content=content, user_id=user.id)
        db.session.add(note)
        db.session.commit()

        return note_schema.dump(note), 201


class NoteDetail(Resource):
    def _get_owned_note(self, note_id):
        user = get_current_user()
        if not user:
            return None, ({'errors': ['Unauthorised. Please log in.']}, 401)

        note = Note.query.get(note_id)
        if not note:
            return None, ({'errors': [f'Note {note_id} not found.']}, 404)

        if note.user_id != user.id:
            return None, ({
                'errors': ['Forbidden. You do not have permission to access this note.']
            }, 403)

        return note, None

    def get(self, note_id):
        note, error = self._get_owned_note(note_id)
        if error:
            return error
        return note_schema.dump(note), 200

    def patch(self, note_id):
        """Update title and/or content. Only provided fields are changed."""
        note, error = self._get_owned_note(note_id)
        if error:
            return error

        data   = request.get_json()
        errors = []

        if 'title' in data:
            if not data['title'].strip():
                errors.append('Title cannot be empty.')
            else:
                note.title = data['title'].strip()

        if 'content' in data:
            if not data['content'].strip():
                errors.append('Content cannot be empty.')
            else:
                note.content = data['content'].strip()
        
        if 'category' in data:
            note.category = data['category'].strip() or 'General'

        if errors:
            return {'errors': errors}, 422

        db.session.commit()
        return note_schema.dump(note), 200

    def delete(self, note_id):
        note, error = self._get_owned_note(note_id)
        if error:
            return error
        db.session.delete(note)
        db.session.commit()
        return {}, 204


# ── Route registration ────────────────────────────────────────────────────────

api.add_resource(Signup,       '/signup',              endpoint='signup')
api.add_resource(Login,        '/login',               endpoint='login')
api.add_resource(Logout,       '/logout',              endpoint='logout')
api.add_resource(CheckSession, '/check_session',       endpoint='check_session')
api.add_resource(NoteList,     '/notes',               endpoint='notes')
api.add_resource(NoteDetail,   '/notes/<int:note_id>', endpoint='note')


if __name__ == '__main__':
    app.run(port=5555, debug=True)