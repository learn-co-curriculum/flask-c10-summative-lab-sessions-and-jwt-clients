from flask import Flask
from models import User
from config import Config
from extensions import bcrypt, db, migrate


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    bcrypt.init_app(app)
    migrate.init_app(app, db)

    @app.get("/")
    def index():
        return {"message": "Backend is running"}

    return app


app = create_app()


if __name__ == "__main__":
    app.run(debug=True)