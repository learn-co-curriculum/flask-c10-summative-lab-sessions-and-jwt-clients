from flask import Flask
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
import os

from server import bcrypt, db, ma
from server.config import Config


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    os.makedirs(os.path.join(os.path.dirname(__file__), "instance"), exist_ok=True)

    db.init_app(app)
    bcrypt.init_app(app)
    ma.init_app(app)
    Migrate(app, db)
    JWTManager(app)

    from server.routes.auth import auth_bp
    from server.routes.tasks import tasks_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(tasks_bp)

    return app


app = create_app()
