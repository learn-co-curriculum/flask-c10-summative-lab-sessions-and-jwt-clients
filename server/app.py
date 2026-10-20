from functools import wraps
from flask import request, session
from flask_restful import Resource

from config import app, db, api
from models import User, Note

def login_required(fn):
    """Reject requests that have no logged-in user in the session."""
    @wraps(fn)
    def wrapper(*args, **kwargs):
        if not session.get("user_id"):
            return {"error": "Unauthorized"}, 401
        return fn(*args, **kwargs)
    return wrapper


class Signup(Resource):
    def post(self):
        data = request.get_json() or {}
        username = data.get("username")
        password = data.get("password")
        if not username or not password:
            return {"error": "Username and password are required."}, 422
        try:
            user = User(username=username)
            user.password_hash = password
            db.session.add(user)
            db.session.commit()
        except ValueError as e:
            db.session.rollback()
            return {"error": str(e)}, 422
        session["user_id"] = user.id
        return user.to_dict(), 201

class Login(Resource):
    def post(self):
        data = request.get_json() or {}
        user = User.query.filter_by(username=data.get("username")).first()
        if user and user.authenticate(data.get("password", "")):
            session["user_id"] = user.id
            return user.to_dict(), 200
        return {"error": "Invalid username or password."}, 401


class Logout(Resource):
    def delete(self):
        session.pop("user_id", None)
        return {}, 204


class CheckSession(Resource):
    def get(self):
        user_id = session.get("user_id")
        user = db.session.get(User, user_id) if user_id else None
        if user:
            return user.to_dict(), 200
        return {"error": "Unauthorized"}, 401


api.add_resource(Signup, "/signup")
api.add_resource(Login, "/login")
api.add_resource(Logout, "/logout")
api.add_resource(CheckSession, "/check_session")



if __name__ == "__main__":
    app.run(port=5555, debug=True)