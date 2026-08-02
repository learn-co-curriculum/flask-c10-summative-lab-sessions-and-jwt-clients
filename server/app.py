import os

from flask import (
    Flask,
    request,
    session,
)
from flask_migrate import Migrate
from flask_restful import (
    Api,
    Resource,
)
from sqlalchemy.exc import IntegrityError

from server.models import (
    User,
    db,
    bcrypt,
)
from server.schemas import user_schema


def create_app(test_config=None):
    app = Flask(__name__)

    app.config["SECRET_KEY"] = (
        os.environ.get(
            "SECRET_KEY",
            "development-secret-key",
        )
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

    def get_current_user():
        user_id = session.get(
            "user_id"
        )

        if user_id is None:
            return None

        user = db.session.get(
            User,
            user_id,
        )

        if user is None:
            session.pop(
                "user_id",
                None,
            )

        return user

    class Home(Resource):

        def get(self):
            return {
                "message": (
                    "Productivity Task Tracker API"
                ),
                "status": "running",
            }, 200

    class Signup(Resource):

        def post(self):
            data = request.get_json(
                silent=True
            )

            if not isinstance(
                data,
                dict,
            ):
                return {
                    "error": (
                        "A JSON request body "
                        "is required."
                    )
                }, 400

            username = data.get(
                "username"
            )

            password = data.get(
                "password"
            )

            password_confirmation = (
                data.get(
                    "password_confirmation"
                )
            )

            if not username:
                return {
                    "error": (
                        "Username is required."
                    )
                }, 400

            if not password:
                return {
                    "error": (
                        "Password is required."
                    )
                }, 400

            if not password_confirmation:
                return {
                    "error": (
                        "Password confirmation "
                        "is required."
                    )
                }, 400

            if (
                password
                != password_confirmation
            ):
                return {
                    "error": (
                        "Passwords do not match."
                    )
                }, 400

            existing_user = (
                User.query.filter_by(
                    username=username.strip()
                ).first()
            )

            if existing_user:
                return {
                    "error": (
                        "Username already exists."
                    )
                }, 409

            try:
                user = User(
                    username=username
                )

                user.password = password

                db.session.add(user)
                db.session.commit()

            except ValueError as error:
                db.session.rollback()

                return {
                    "error": str(error)
                }, 400

            except IntegrityError:
                db.session.rollback()

                return {
                    "error": (
                        "Username already exists."
                    )
                }, 409

            session["user_id"] = user.id

            return (
                user_schema.dump(user),
                201,
            )

    class Login(Resource):

        def post(self):
            data = request.get_json(
                silent=True
            )

            if not isinstance(
                data,
                dict,
            ):
                return {
                    "error": (
                        "A JSON request body "
                        "is required."
                    )
                }, 400

            username = data.get(
                "username"
            )

            password = data.get(
                "password"
            )

            if not username or not password:
                return {
                    "error": (
                        "Username and password "
                        "are required."
                    )
                }, 400

            user = (
                User.query.filter_by(
                    username=username.strip()
                ).first()
            )

            if (
                user is None
                or not user.authenticate(
                    password
                )
            ):
                return {
                    "error": (
                        "Invalid username "
                        "or password."
                    )
                }, 401

            session["user_id"] = user.id

            return (
                user_schema.dump(user),
                200,
            )

    class CheckSession(Resource):

        def get(self):
            user = get_current_user()

            if user is None:
                return {}, 200

            return (
                user_schema.dump(user),
                200,
            )

    class Logout(Resource):

        def delete(self):
            session.pop(
                "user_id",
                None,
            )

            return {}, 200

    api.add_resource(
        Home,
        "/",
    )

    api.add_resource(
        Signup,
        "/signup",
    )

    api.add_resource(
        Login,
        "/login",
    )

    api.add_resource(
        CheckSession,
        "/check_session",
    )

    api.add_resource(
        Logout,
        "/logout",
    )

    return app


app = create_app()


if __name__ == "__main__":
    app.run(
        port=5555,
        debug=True,
    )