from functools import wraps

from config import db
from flask import request, session
from models import User


def paginate(query, schema):
    """Return one page of a query, using ?page= and ?per_page= from the URL."""
    page = max(request.args.get("page", 1, type=int), 1)
    per_page = min(max(request.args.get("per_page", 10, type=int), 1), 50)
    result = query.paginate(page=page, per_page=per_page, error_out=False)
    return {
        "items": schema.dump(result.items),
        "page": result.page,
        "per_page": result.per_page,
        "total": result.total,
        "pages": result.pages,
    }


def current_user():
    user_id = session.get("user_id")
    if user_id is None:
        return None
    return db.session.get(User, user_id)


def login_required(func):
    """Block the request with 401 unless a user is logged in."""

    @wraps(func)
    def wrapper(*args, **kwargs):
        if current_user() is None:
            return {"errors": ["You must be logged in."]}, 401
        return func(*args, **kwargs)

    return wrapper

def find_owned(model, record_id):
    """Find a record by id only if it belongs to the logged-in user.

    Returning None for other users' records (rather than 403) avoids
    revealing that the record exists.
    """
    return model.query.filter_by(
        id=record_id, user_id=session.get("user_id")
    ).first()