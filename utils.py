"""Shared helpers: error formatting and the login_required decorator."""
from functools import wraps

from flask import g, session

from config import db
from models import User


def format_errors(messages):
    """Flatten marshmallow's {field: [msgs]} into a list of strings.

    The frontend expects errors as a plain list: {"errors": ["...", "..."]}.
    """
    errors = []
    for field, msgs in messages.items():
        if not isinstance(msgs, (list, tuple)):
            msgs = [str(msgs)]
        for msg in msgs:
            errors.append(str(msg) if field == "_schema" else f"{field}: {msg}")
    return errors


def login_required(fn):
    """Reject the request with 401 unless the session holds a valid user."""

    @wraps(fn)
    def wrapper(*args, **kwargs):
        user_id = session.get("user_id")
        user = db.session.get(User, user_id) if user_id else None
        if user is None:
            return {"errors": ["Unauthorized: please log in."]}, 401
        g.current_user = user  # available to the route as g.current_user
        return fn(*args, **kwargs)

    return wrapper