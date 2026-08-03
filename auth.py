from functools import wraps

from flask import jsonify, session

from models import User


def current_user():
    user_id = session.get("user_id")
    return db_user if user_id and (db_user := User.query.get(user_id)) else None


def login_required(view):
    @wraps(view)
    def wrapped_view(*args, **kwargs):
        if current_user() is None:
            return jsonify({"error": "Authentication required."}), 401
        return view(*args, **kwargs)

    return wrapped_view
