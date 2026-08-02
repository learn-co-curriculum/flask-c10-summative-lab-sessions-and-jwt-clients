from flask import Flask, jsonify
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate

from config import Config
from server.controllers.auth_controller import auth_bp
from server.controllers.task_controller import task_bp
from server.extensions import bcrypt, db


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    CORS(app)
    db.init_app(app)
    bcrypt.init_app(app)
    jwt = JWTManager(app)
    Migrate(app, db)

    # The supplied JWT client calls these routes without an /api prefix.
    app.register_blueprint(auth_bp)
    app.register_blueprint(task_bp)

    @jwt.expired_token_loader
    def expired_token_callback(_jwt_header, _jwt_payload):
        return jsonify({"errors": ["The token has expired."]}), 401

    @jwt.invalid_token_loader
    def invalid_token_callback(_error):
        return jsonify({"errors": ["Invalid token."]}), 422

    @jwt.unauthorized_loader
    def missing_token_callback(_error):
        return jsonify({"errors": ["Request does not contain an access token."]}), 401

    @app.get("/")
    def home():
        return jsonify({"message": "Welcome to the Productivity App API!"}), 200

    return app


app = create_app()
