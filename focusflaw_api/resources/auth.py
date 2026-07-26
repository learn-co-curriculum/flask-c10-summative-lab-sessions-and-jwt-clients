from flask import Blueprint, request, jsonify, session

from extensions import db
from models import User
from schemas import UserSchema

auth_bp = Blueprint("auth", __name__)

user_schema = UserSchema()


@auth_bp.route("/signup", methods=["POST"])
def signup():
    data = request.get_json()

    username = data.get("username")
    email = data.get("email")
    password = data.get("password")

    if User.query.filter_by(username=username).first():
        return jsonify({"Error": "Username already exists"}), 400

    if User.query.filter_by(email=email).first():
        return jsonify({"Error": "Email already exists"}), 400

    user = User(
        username=username,
        email=email
    )

    user.set_password(password)

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

    if not user or not user.check_password(password):
        return jsonify({"Error": "Invalid username or password"}), 401

    session["user_id"] = user.id

    return user_schema.dump(user), 200


@auth_bp.route("/check_session", methods=["GET"])
def check_session():
    user_id = session.get("user_id")

    if not user_id:
        return jsonify({"Error": "Unauthorized"}), 401

    user = User.query.get(user_id)

    if not user:
        return jsonify({"Error": "User not found"}), 404

    return user_schema.dump(user), 200


@auth_bp.route("/logout", methods=["DELETE"])
def logout():
    session.pop("user_id", None)

    return jsonify({
        "message": "Logged out successfully"
    }), 200