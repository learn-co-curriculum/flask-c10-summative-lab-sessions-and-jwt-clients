from flask import request, session
from flask_restful import Resource
from sqlalchemy.exc import IntegrityError

from config import db
from helpers import current_user
from models import User
from schemas import UserSchema

user_schema = UserSchema()


class Signup(Resource):
    def post(self):
        data = request.get_json() or {}
        username = data.get("username")
        password = data.get("password")

        if password != data.get("password_confirmation"):
            return {"errors": ["Passwords do not match."]}, 422
        if username and User.query.filter_by(username=username.strip()).first():
            return {"errors": ["Username is already taken."]}, 422

        try:
            user = User(username=username)
            user.password_hash = password
            db.session.add(user)
            db.session.commit()
        except ValueError as error:
            db.session.rollback()
            return {"errors": [str(error)]}, 422
        except IntegrityError:
            db.session.rollback()
            return {"errors": ["Username is already taken."]}, 422

        session["user_id"] = user.id
        return user_schema.dump(user), 201


class Login(Resource):
    def post(self):
        data = request.get_json() or {}
        user = User.query.filter_by(username=(data.get("username") or "").strip()).first()

        if user and user.authenticate(data.get("password") or ""):
            session["user_id"] = user.id
            return user_schema.dump(user), 200
        return {"errors": ["Invalid username or password."]}, 401


class CheckSession(Resource):
    def get(self):
        user = current_user()
        if user:
            return user_schema.dump(user), 200
        return {"errors": ["Not logged in."]}, 401


class Logout(Resource):
    def delete(self):
        if current_user() is None:
            return {"errors": ["Not logged in."]}, 401
        session.pop("user_id", None)
        return {}, 204