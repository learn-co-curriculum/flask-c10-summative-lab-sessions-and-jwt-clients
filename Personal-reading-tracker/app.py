import os
from datetime import timedelta

from flask import Flask

try:
    from flask_migrate import Migrate  # type: ignore[reportMissingModuleSource]
except ModuleNotFoundError:
    class Migrate:
        def __init__(self, *args, **kwargs):
            pass

from auth import auth, bcrypt, protect_routes
from models import db


def create_app(test_config=None):
    app = Flask(__name__)
    app.config.from_mapping(
        SQLALCHEMY_DATABASE_URI=os.getenv('DATABASE_URL', 'sqlite:///app.db'),
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
        SECRET_KEY=os.getenv('SECRET_KEY'),
        SESSION_COOKIE_HTTPONLY=True,
        SESSION_COOKIE_SAMESITE='Lax',
        SESSION_COOKIE_SECURE=os.getenv('COOKIE_SECURE', 'false').lower() == 'true',
        PERMANENT_SESSION_LIFETIME=timedelta(hours=8),
        SESSION_REFRESH_EACH_REQUEST=False,
        MAX_CONTENT_LENGTH=16 * 1024,
        TRUSTED_ORIGINS=os.getenv('TRUSTED_ORIGINS', 'http://localhost:4000,http://localhost:5555').split(','),
    )
    if test_config:
        app.config.update(test_config)
    if not app.config['SECRET_KEY']:
        raise RuntimeError('Set SECRET_KEY to a random secret before starting the API.')
    db.init_app(app)
    bcrypt.init_app(app)
    Migrate(app, db)
    app.register_blueprint(auth)
    app.before_request(protect_routes)
    return app


app = create_app()

if __name__ == '__main__':
    app.run(port=5555)
