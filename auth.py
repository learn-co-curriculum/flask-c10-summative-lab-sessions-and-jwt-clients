from flask import Blueprint, request, jsonify
from extensions import db
from models import User
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity

auth_bp = Blueprint('auth_bp', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    if not data or not data.get('username') or not data.get('email') or not data.get('password'):
        return {"error": "username, email and password are required"}, 400

    if User.query.filter((User.username == data['username']) | (User.email == data['email'])).first():
        return {"error": "User with this username or email already exists"}, 400

    user = User(username=data['username'], email=data['email'])
    user.set_password = data['password']
    db.session.add(user)
    db.session.commit()

    token = create_access_token(identity=user.id)
    return {"id": user.id, "username": user.username, "email": user.email, "access_token": token}, 201

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    if not data or not data.get('username') or not data.get('password'):
        return {"error": "username and password are required"}, 400

    user = User.query.filter_by(username=data['username']).first()
    if user and user.check_password(data['password']):
        token = create_access_token(identity=user.id)
        return {"id": user.id, "username": user.username, "email": user.email, "access_token": token}, 200
    else:
        return {"error": "Invalid username or password"}, 401

@auth_bp.route('/protected', methods=['GET'])
@jwt_required()
def protected():
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)
    if not user:
        return {"error": "User not found"}, 404
    return {"message": f"Hello, {user.username}! This is a protected route."}, 200

@auth_bp.route('/logout', methods=['POST'])
@jwt_required()
def logout():
    # In a real application, you would handle token revocation here.
    return {"message": "Logout successful"}, 200
