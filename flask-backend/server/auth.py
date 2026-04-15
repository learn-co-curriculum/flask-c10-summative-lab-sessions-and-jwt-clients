from flask import Blueprint, request, session, jsonify
from models import db, User

auth_bp = Blueprint("auth", __name__)


#create signup route
@auth_bp.route("/signup", methods=["POST"])
def signup():
    data = request.get_json()

    username = data.get("username")
    password = data.get("password")
    password_confirmation = data.get("password_confirmation")

    if not username or not password:
        return jsonify({"error": "Missing fields"}), 400

    if password != password_confirmation:
        return jsonify({"error": "Passwords do not match"}), 400

    # check duplicate user
    if User.query.filter_by(username=username).first():
        return jsonify({"error": "User already exists"}), 409

    # create user
    new_user = User(username=username)
    new_user.set_password(password)

    db.session.add(new_user)
    db.session.commit()

    # create session for auto login
    session["user_id"] = new_user.id
    return jsonify({"id": new_user.id, "username": new_user.username}), 201

#create login route
@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()

    username = data.get("username")
    password = data.get("password")

    user = User.query.filter_by(username=username).first()
    if not user or not user.check_password(password):
        return jsonify({"error": "Invalid credentials"}), 401

    # create session
    session["user_id"] = user.id
    return jsonify({"id": user.id, "username": user.username}), 200

#check session -> read session -> return user if exists
@auth_bp.route("/check_session", methods=["GET"])
def check_session():
    user_id = session.get("user_id")
    if not user_id:
        return jsonify({}), 200
    user = User.query.get(user_id)
    if not user:
        return jsonify({}), 200
    
    return jsonify({"id": user.id, "username": user.username}), 200

#logout -> remove session route
@auth_bp.route("/logout", methods=["DELETE"])
def logout():
    session.pop("user_id", None)
    return jsonify({}), 200