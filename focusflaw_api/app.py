from flask import Flask

from config import Config
from extensions import db, migrate, bcrypt

from models import User, Task
from resources.auth import auth_bp
from resources.task import task_bp


def create_app():
    app = Flask(__name__)

    app.config.from_object(Config)

    # Secret key used to sign session cookies
    app.secret_key = "focusflow-secret-key"

    db.init_app(app)
    migrate.init_app(app, db)
    bcrypt.init_app(app)

    app.register_blueprint(auth_bp)
    app.register_blueprint(task_bp)

    @app.route("/")
    def home():
        return {
            "message": "FocusFlow API is running!"
        }

    return app


app = create_app()


if __name__ == "__main__":
    app.run(debug=True, port=5555)