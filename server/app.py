import os

from flask import Flask
from flask_migrate import Migrate
from flask_restful import Api, Resource

from server.models import db, bcrypt


def create_app(test_config=None):
    app = Flask(__name__)

    app.config["SECRET_KEY"] = os.environ.get(
        "SECRET_KEY",
        "development-secret-key",
    )

    app.config[
        "SQLALCHEMY_DATABASE_URI"
    ] = os.environ.get(
        "DATABASE_URI",
        "sqlite:///app.db",
    )

    app.config[
        "SQLALCHEMY_TRACK_MODIFICATIONS"
    ] = False

    if test_config:
        app.config.update(
            test_config
        )

    db.init_app(app)
    bcrypt.init_app(app)

    Migrate(app, db)

    api = Api(app)

    class Home(Resource):

        def get(self):
            return {
                "message": (
                    "Productivity Task Tracker API"
                ),
                "status": "running",
            }, 200

    api.add_resource(
        Home,
        "/",
    )

    return app


app = create_app()


if __name__ == "__main__":
    app.run(
        port=5555,
        debug=True,
    )