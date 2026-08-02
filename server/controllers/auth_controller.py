from flask import Blueprint, jsonify, request
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required
from server.models.user import User
from server.extensions import db

auth_bp = Blueprint('auth', __name__)


def auth_error(message, status_code):
    """Return the error shape used by the supplied JWT client."""
    return jsonify({"errors": [message]}), status_code


@auth_bp.route('/signup', methods=['POST'])
def signup():
    data = request.get_json(silent=True) or {}
    username = data.get('username')
    password = data.get('password')
    password_confirmation = data.get('password_confirmation')

    if not username or not password or not password_confirmation:
        return auth_error("Username, password, and password confirmation are required.", 400)

    if password != password_confirmation:
        return auth_error("Passwords do not match.", 400)

    if User.query.filter_by(username=username).first():
        return auth_error("Username already exists.", 400)

    try:
        new_user = User(username=username)
        new_user.password = password
        db.session.add(new_user)
        db.session.commit()

        access_token = create_access_token(identity=new_user.id)
        return jsonify({"token": access_token, "user": new_user.to_dict()}), 201
    except Exception:
        db.session.rollback()
        return auth_error("Unable to create user.", 500)

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json(silent=True) or {}
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return auth_error("Username and password are required.", 400)

    user = User.query.filter_by(username=username).first()

    if not user or not user.check_password(password):
        return auth_error("Invalid username or password.", 401)

    access_token = create_access_token(identity=user.id)
    return jsonify({"token": access_token, "user": user.to_dict()}), 200

@auth_bp.route('/me', methods=['GET'])
@jwt_required()
def get_current_user():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)

    if not user:
        return auth_error("User not found.", 404)

    return jsonify(user.to_dict()), 200

@auth_bp.route('/logout', methods=['DELETE'])
@jwt_required()
def logout():
    return jsonify({}), 200
