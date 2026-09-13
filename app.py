import os
from flask import Flask
from config import Config
from extensions import db, migrate, bcrypt, jwt
from flask_cors import CORS
from auth import auth_bp
from notes import notes_bp

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    CORS(app)  # Enable CORS for all routes

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    bcrypt.init_app(app)
    jwt.init_app(app)

    # Register blueprints
    app.register_blueprint(auth_bp)
    app.register_blueprint(notes_bp)

    @app.route('/')
    def index():
        return "Welcome to the Flask JWT Notes API!"

    return app

app = create_app()

if __name__ == '__main__':
    app.run(port = 5000, debug=True)