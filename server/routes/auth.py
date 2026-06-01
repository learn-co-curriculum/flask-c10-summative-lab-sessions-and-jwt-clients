from flask import Blueprint, request
from models import User
from config import db
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity

auth_bp = Blueprint("auth", __name__)


@auth_bp.post("/signup")
def signup():
    data = request.get_json()

    try:
        user = User(username=data.get("username"))
        user.password_hash = data.get("password")

        db.session.add(user)
        db.session.commit()

        token = create_access_token(identity=str(user.id))

        return {
            "message": "User created successfully",
            "token": token,
            "user": {"id": user.id, "username": user.username}
        }, 201

    except Exception as e:
        return {"error": str(e)}, 400


@auth_bp.post("/login")
def login():
    data = request.get_json()

    user = User.query.filter_by(username=data.get("username")).first()

    if user and user.authenticate(data.get("password")):
        token = create_access_token(identity=str(user.id))

        return {
            "token": token,
            "user": {"id": user.id, "username": user.username}
        }, 200

    return {"error": "Invalid credentials"}, 401


@auth_bp.get("/me")
@jwt_required()
def me():
    user_id = get_jwt_identity()
    user = User.query.get(int(user_id))

    if not user:
        return {"error": "User not found"}, 404

    return {
        "id": user.id,
        "username": user.username
    }, 200