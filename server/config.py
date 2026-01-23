import os

# Basic Flask config
BASE_DIR = os.path.abspath(os.path.dirname(__file__))

class Config:
    # SECURITY
    SECRET_KEY = os.environ.get("SECRET_KEY", "dev-secret-key")

    # SQLite DB file inside /server
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DATABASE_URL",
        f"sqlite:///{os.path.join(BASE_DIR, 'app.db')}"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # JWT config
    JWT_SECRET_KEY = os.environ.get("JWT_SECRET_KEY", "dev-jwt-secret-key")