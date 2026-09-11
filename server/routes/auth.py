from flask import Blueprint, jsonify, request, session
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from sqlalchemy import or_

from server import db
from server.models.user import User
from server.schemas import registration_data


auth_bp = Blueprint("auth", __name__)


def user_response(user, token=None):
	data = user.to_dict()
	if token:
		data["token"] = token
		data["user"] = user.to_dict()
	return data


def validation_error(message, status=422):
	return jsonify({"errors": [message]}), status


def authenticate_user():
	username = request.json.get("username") if request.is_json else None
	password = request.json.get("password") if request.is_json else None
	if not username or not password:
		return None, validation_error("Username and password are required.")

	user = User.query.filter_by(username=username).first()
	if not user or not user.check_password(password):
		return None, validation_error("Invalid username or password.", 401)
	return user, None


@auth_bp.post("/signup")
def signup():
	payload, error = registration_data(request.get_json(silent=True))
	if error:
		return validation_error(error)
	username = payload["username"]
	if User.query.filter(or_(User.username == username, User.email == payload["email"])).first():
		return validation_error("Username or email is already taken.", 409)

	user = User(username=username, email=payload["email"])
	user.set_password(payload["password"])
	db.session.add(user)
	db.session.commit()
	token = create_access_token(identity=str(user.id))
	session["user_id"] = user.id
	return jsonify(user_response(user, token)), 201


@auth_bp.post("/login")
def login():
	user, error = authenticate_user()
	if error:
		return error
	token = create_access_token(identity=str(user.id))
	session["user_id"] = user.id
	return jsonify(user_response(user, token))


@auth_bp.get("/me")
@jwt_required()
def me():
	user = db.session.get(User, int(get_jwt_identity()))
	if not user:
		return validation_error("User not found.", 404)
	return jsonify(user.to_dict())


@auth_bp.get("/check_session")
def check_session():
	user_id = session.get("user_id")
	user = db.session.get(User, user_id) if user_id else None
	if not user:
		return jsonify({"errors": ["Authentication required."]}), 401
	return jsonify(user.to_dict())


@auth_bp.delete("/logout")
def logout():
	session.pop("user_id", None)
	return "", 204
