from flask import Flask
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
import os

from server import bcrypt, db, ma
from server.config import Config

from server.routes.auth import auth_bp


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    os.makedirs(os.path.join(os.path.dirname(__file__), "instance"), exist_ok=True)

    db.init_app(app)
    bcrypt.init_app(app)
    ma.init_app(app)
    Migrate(app, db)
    jwt = JWTManager(app)

    @jwt.unauthorized_loader
    def missing_token(message):
        return {"errors": ["Authentication required."]}, 401

    @jwt.invalid_token_loader
    def invalid_token(message):
        return {"errors": ["Invalid or expired token."]}, 401

    @jwt.expired_token_loader
    def expired_token(jwt_header, jwt_payload):
        return {"errors": ["Invalid or expired token."]}, 401

    from server.routes.auth import auth_bp
    from server.routes.tasks import tasks_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(tasks_bp)

    return app


app = create_app()
