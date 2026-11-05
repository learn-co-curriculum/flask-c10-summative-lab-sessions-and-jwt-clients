"""Authentication routes: signup, login, logout and check_session."""
from flask import request, session
from flask_restful import Resource
from sqlalchemy.exc import IntegrityError

from config import db
from models import User
from schemas import user_schema


class Signup(Resource):
    """POST /signup - create a user and log them in."""

    def post(self):
        data = request.get_json(silent=True)
        data = data if isinstance(data, dict) else {}

        username = data.get("username")
        password = data.get("password")
        confirmation = data.get("password_confirmation")

        errors = []
        if not isinstance(username, str) or len(username.strip()) < 3:
            errors.append("Username must be at least 3 characters.")
        elif User.query.filter_by(username=username.strip()).first():
            errors.append("Username is already taken.")
        if not isinstance(password, str) or len(password) < 6:
            errors.append("Password must be at least 6 characters.")
        # Confirmation is only checked when the client sends it.
        elif confirmation is not None and password != confirmation:
            errors.append("Password and confirmation do not match.")
        if errors:
            return {"errors": errors}, 422

        try:
            user = User(username=username)
            user.password_hash = password  # hashed by the model's setter
            db.session.add(user)
            db.session.commit()
        except (IntegrityError, ValueError):
            db.session.rollback()
            return {"errors": ["Could not create user."]}, 422

        session["user_id"] = user.id
        return user_schema.dump(user), 201


class Login(Resource):
    """POST /login - verify credentials and start a session."""

    def post(self):
        data = request.get_json(silent=True)
        data = data if isinstance(data, dict) else {}

        username = data.get("username")
        password = data.get("password")

        user = None
        if isinstance(username, str) and isinstance(password, str):
            user = User.query.filter_by(username=username.strip()).first()

        # Same message for unknown user and wrong password (no user enumeration).
        if user is None or not user.authenticate(password):
            return {"errors": ["Invalid username or password."]}, 401

        session["user_id"] = user.id
        return user_schema.dump(user), 200


class Logout(Resource):
    """DELETE /logout - clear the session."""

    def delete(self):
        session.pop("user_id", None)
        return "", 204


class CheckSession(Resource):
    """GET /check_session - return the logged-in user, or 401 if none."""

    def get(self):
        user_id = session.get("user_id")
        user = db.session.get(User, user_id) if user_id else None
        if user is None:
            return {}, 401
        return user_schema.dump(user), 200