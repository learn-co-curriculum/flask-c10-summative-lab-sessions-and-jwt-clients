from flask import Flask
from flask_jwt_extended import JWTManager
from config import Config
from extensions import bcrypt, db, migrate
from models import User
from routes import register_routes


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    app.config["JWT_SECRET_KEY"] = "super-secret-key-change-me"

    db.init_app(app)
    bcrypt.init_app(app)
    migrate.init_app(app, db)
    JWTManager(app)

    register_routes(app)

    @app.get("/")
    def index():
        return {"message": "Backend is running"}

    return app


app = create_app()


if __name__ == "__main__":
    app.run(debug=True)