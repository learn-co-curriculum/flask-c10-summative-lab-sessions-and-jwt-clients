import os
import secrets


class Config:
    """Application configuration shared by development and production."""

    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL", "sqlite:///notes.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # A deployment must set SECRET_KEY so sessions remain valid across restarts.
    # The random fallback keeps local development from using a known secret.
    SECRET_KEY = os.environ.get("SECRET_KEY", secrets.token_urlsafe(32))
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = "Lax"
    SESSION_COOKIE_SECURE = os.environ.get("SESSION_COOKIE_SECURE", "false").lower() == "true"
