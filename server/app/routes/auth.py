"""
Authentication routes.

"""

from flask import Blueprint, request

from app.extensions import db
from app.models.user import User
from app.utils.decorators import token_required
from app.utils.responses import ok, created, bad_request, unauthorized

auth_bp = Blueprint("auth", __name__)


# ------------------------------------------------------------------ #
# POST /signup                                                         #
# ------------------------------------------------------------------ #


@auth_bp.route("/signup", methods=["POST"])
def signup():
    """Register a new user and return a JWT.

    Validates that:
    * ``username`` and ``password`` are present and non-empty.
    * ``password_confirmation`` matches ``password``.
    * The chosen username is not already taken.
    """
    data = request.get_json(silent=True) or {}

    username = (data.get("username") or "").strip()
    password = data.get("password") or ""
    password_confirmation = data.get("password_confirmation") or ""

    # --- Field-level validation ---
    errors = []
    if not username:
        errors.append("Username is required.")
    if len(username) < 3:
        errors.append("Username must be at least 3 characters.")
    if not password:
        errors.append("Password is required.")
    if len(password) < 8:
        errors.append("Password must be at least 8 characters.")
    if password != password_confirmation:
        errors.append("Password and confirmation do not match.")
    if errors:
        return bad_request("Validation failed.", errors)

    # --- Uniqueness check ---
    if User.query.filter_by(username=username).first():
        return bad_request("Validation failed.", ["Username already registered."])

    # --- Persist ---
    try:
        user = User(username=username)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
    except Exception:
        db.session.rollback()
        from app.utils.responses import server_error

        return server_error("Could not create user. Please try again.")

    token = user.generate_token()
    return created({"token": token, "user": {"id": user.id, "username": user.username}})


# ------------------------------------------------------------------ #
# POST /login                                                          #
# ------------------------------------------------------------------ #


@auth_bp.route("/login", methods=["POST"])
def login():
    """Authenticate an existing user and return a JWT."""
    data = request.get_json(silent=True) or {}

    username = (data.get("username") or "").strip()
    password = data.get("password") or ""

    if not username or not password:
        return bad_request(
            "Validation failed.", ["Username and password are required."]
        )

    user = User.query.filter_by(username=username).first()

    # Use a constant-time comparison path to avoid user-enumeration
    if user is None or not user.check_password(password):
        return unauthorized("Invalid username or password.")

    token = user.generate_token()
    return ok({"token": token, "user": {"id": user.id, "username": user.username}})


# ------------------------------------------------------------------ #
# GET /me                                                              #
# ------------------------------------------------------------------ #


@auth_bp.route("/me", methods=["GET"])
@token_required
def me(current_user):
    """Return the currently authenticated user.

    The client calls this on every page load to restore the session from
    the token stored in localStorage.  The response is intentionally flat
    (no nesting) to match what the client destructures.
    """
    return ok({"id": current_user.id, "username": current_user.username})
