from functools import wraps
from flask import request, session
from flask_restful import Resource

from config import app, db, api
from models import User, Note

def login_required(fn):
    """Reject requests that have no logged-in user in the session."""
    @wraps(fn)
    def wrapper(*args, **kwargs):
        if not session.get("user_id"):
            return {"error": "Unauthorized"}, 401
        return fn(*args, **kwargs)
    return wrapper


class Signup(Resource):
    def post(self):
        data = request.get_json() or {}
        username = data.get("username")
        password = data.get("password")
        if not username or not password:
            return {"error": "Username and password are required.",
                    "errors": ["Username and password are required."]}, 422
        try:
            user = User(username=username)
            user.password_hash = password
            db.session.add(user)
            db.session.commit()
        except ValueError as e:
            db.session.rollback()
            return {"error": str(e), "errors": [str(e)]}, 422
        session["user_id"] = user.id
        return user.to_dict(), 201


class Login(Resource):
    def post(self):
        data = request.get_json() or {}
        user = User.query.filter_by(username=data.get("username")).first()
        if user and user.authenticate(data.get("password", "")):
            session["user_id"] = user.id
            return user.to_dict(), 200
        return {"error": "Invalid username or password.",
                "errors": ["Invalid username or password."]}, 401


class Logout(Resource):
    def delete(self):
        session.pop("user_id", None)
        return {}, 204


class CheckSession(Resource):
    def get(self):
        user_id = session.get("user_id")
        user = db.session.get(User, user_id) if user_id else None
        if user:
            return user.to_dict(), 200
        return {"error": "Unauthorized"}, 401

class NoteList(Resource):
    @login_required
    def get(self):
        page = request.args.get("page", 1, type=int)
        per_page = request.args.get("per_page", 5, type=int)
        pagination = (Note.query
                      .filter_by(user_id=session["user_id"])
                      .order_by(Note.created_at.desc())
                      .paginate(page=page, per_page=per_page, error_out=False))
        return {
            "page": pagination.page,
            "per_page": pagination.per_page,
            "total": pagination.total,
            "pages": pagination.pages,
            "notes": [n.to_dict() for n in pagination.items],
        }, 200

    @login_required
    def post(self):
        data = request.get_json() or {}
        try:
            note = Note(title=data.get("title"),
                        content=data.get("content"),
                        user_id=session["user_id"])
            db.session.add(note)
            db.session.commit()
        except ValueError as e:
            db.session.rollback()
            return {"error": str(e)}, 422
        return note.to_dict(), 201


class NoteByID(Resource):
    def _get_own_note(self, id):
        """Filtering by user_id makes other users' notes look nonexistent."""
        return Note.query.filter_by(id=id, user_id=session["user_id"]).first()

    @login_required
    def get(self, id):
        note = self._get_own_note(id)
        if not note:
            return {"error": "Note not found."}, 404
        return note.to_dict(), 200

    @login_required
    def patch(self, id):
        note = self._get_own_note(id)
        if not note:
            return {"error": "Note not found."}, 404
        data = request.get_json() or {}
        try:
            for field in ("title", "content"):
                if field in data:
                    setattr(note, field, data[field])
            db.session.commit()
        except ValueError as e:
            db.session.rollback()
            return {"error": str(e)}, 422
        return note.to_dict(), 200

    @login_required
    def delete(self, id):
        note = self._get_own_note(id)
        if not note:
            return {"error": "Note not found."}, 404
        db.session.delete(note)
        db.session.commit()
        return {}, 204


api.add_resource(Signup, "/signup")
api.add_resource(Login, "/login")
api.add_resource(Logout, "/logout")
api.add_resource(CheckSession, "/check_session")
api.add_resource(NoteList, "/notes")
api.add_resource(NoteByID, "/notes/<int:id>")



if __name__ == "__main__":
    app.run(port=5555, debug=True)