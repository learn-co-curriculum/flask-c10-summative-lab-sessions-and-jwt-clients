from flask import Blueprint, request, session
from server.models import db, User
from server.schemas import user_schema

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/signup", methods=["POST"])
def signup():
    data = request.get_json()

    username = data.get("username")
    password = data.get("password")

    if not username or not password:
        return {"error": "Username and password are required"}, 422

    if User.query.filter_by(username=username).first():
        return {"error": "Username already exists"}, 422

    user = User(username=username)
    user.password_hash = password

    db.session.add(user)
    db.session.commit()

    session["user_id"] = user.id

    return user_schema.dump(user), 201

@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()

    username = data.get("username")
    password = data.get("password")

    user = User.query.filter_by(username=username).first()

    if user and user.authenticate(password):
        session["user_id"] = user.id
        return user_schema.dump(user), 200

    return {"error": "Invalid username or password"}, 401

@auth_bp.route("/logout", methods=["DELETE"])
def logout():
    session.pop("user_id", None)
    return {}, 204

@auth_bp.route("/check_session", methods=["GET"])
def check_session():
    user_id = session.get("user_id")

    if not user_id:
        return {"error": "Unauthorized"}, 401

    user = User.query.get(user_id)

    return user_schema.dump(user), 200

