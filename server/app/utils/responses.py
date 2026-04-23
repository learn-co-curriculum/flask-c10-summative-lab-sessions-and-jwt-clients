"""
HTTP response helpers.

These thin wrappers around ``flask.jsonify`` provide a consistent call-site
API and ensure that every response uses the correct HTTP status code.

  This keeps the backend contract simple and easy to test.
"""
from flask import jsonify


def ok(data: dict) -> tuple:
    """200 OK — successful read or update."""
    return jsonify(data), 200


def created(data: dict) -> tuple:
    """201 Created — successful resource creation."""
    return jsonify(data), 201


def no_content() -> tuple:
    """204 No Content — successful deletion."""
    return "", 204


def bad_request(message: str, errors: dict = None) -> tuple:
    """400 Bad Request — validation failure or missing fields."""
    body = {"errors": [message]}
    if errors:
        body["errors"] = errors
    return jsonify(body), 400


def unauthorized(message: str = "Unauthorized") -> tuple:
    """401 Unauthorized — missing, invalid, or expired token."""
    return jsonify({"errors": [message]}), 401


def not_found(message: str = "Resource not found") -> tuple:
    """404 Not Found — resource does not exist or is not owned by the user."""
    return jsonify({"errors": [message]}), 404


def server_error(message: str = "Internal server error") -> tuple:
    """500 Internal Server Error — unexpected failure."""
    return jsonify({"errors": [message]}), 500
