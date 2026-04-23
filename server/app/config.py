import os
from datetime import timedelta


class Config:
    """Base configuration shared by all environments."""

    # Flask core
    SECRET_KEY = os.environ.get("SECRET_KEY", "dev-fallback-secret-key")

    # SQLAlchemy
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # JWT
    JWT_SECRET_KEY = os.environ.get("JWT_SECRET_KEY", "dev-fallback-jwt-secret-key-32chars")
    JWT_EXPIRATION_DELTA = timedelta(hours=24)

    # Pagination defaults
    ITEMS_PER_PAGE = 10
    MAX_ITEMS_PER_PAGE = 100


class DevelopmentConfig(Config):
    """Development configuration — uses a local SQLite database."""

    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DATABASE_URL", "sqlite:///dev.db"
    )


class TestingConfig(Config):
    """Testing configuration — uses an in-memory SQLite database."""

    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
    # Disable CSRF protection in tests
    WTF_CSRF_ENABLED = False


class ProductionConfig(Config):
    """Production configuration — requires DATABASE_URL to be set."""

    DEBUG = False
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL")


def get_config() -> Config:
    """Return the appropriate config class based on FLASK_ENV."""
    env = os.environ.get("FLASK_ENV", "development").lower()
    config_map = {
        "development": DevelopmentConfig,
        "testing": TestingConfig,
        "production": ProductionConfig,
    }
    return config_map.get(env, DevelopmentConfig)
