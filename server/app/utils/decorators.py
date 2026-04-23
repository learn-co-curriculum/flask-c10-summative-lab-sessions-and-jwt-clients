"""
Authentication decorator.

``token_required`` extracts the JWT from the ``Authorization: Bearer <token>``
header, verifies it, and injects the resolved ``User`` object as the first
positional argument to the wrapped view function.

Any route decorated with ``@token_required`` will automatically return 401
when no valid token is present.
"""

from functools import wraps
from typing import Union

from flask import request

from app.extensions import db
from app.models.user import User
from app.utils.responses import unauthorized


def token_required(f):
    """Protect a route with JWT authentication.

    Usage::

        @notes_bp.route("/<int:note_id>", methods=["GET"])
        @token_required
        def get_note(current_user, note_id):
            ...
    """

    @wraps(f)
    def decorated(*args, **kwargs):
        token = _extract_token()

        if token is None:
            return unauthorized("Authorization header missing or malformed.")

        payload = User.verify_token(token)
        if payload is None:
            return unauthorized("Token is invalid or has expired.")

        current_user = db.session.get(User, payload.get("user_id"))
        if current_user is None:
            return unauthorized("User associated with this token no longer exists.")

        return f(current_user, *args, **kwargs)

    return decorated


# ------------------------------------------------------------------ #
# Private helpers                                                      #
# ------------------------------------------------------------------ #


def _extract_token() -> Union[str, None]:
    """Parse the Bearer token from the Authorization header.

    Returns the raw token string, or *None* if the header is absent or
    does not follow the ``Bearer <token>`` format.
    """
    auth_header = request.headers.get("Authorization", "")
    parts = auth_header.split()
    if len(parts) == 2 and parts[0].lower() == "bearer":
        return parts[1]
    return None
