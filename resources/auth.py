from flask_restful import Resource
from flask import request
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from models import User, db
from flask_bcrypt import generate_password_hash, check_password_hash

class SignupResource(Resource):
    """Handle user signup"""
    def post(self):
        # Get data from request
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')
        # Check if username and password provided
        if not username or not password:
            return {"error": "Username and password required"}, 400
        # Check if user already exists
        if User.query.filter_by(username=username).first():
            return {"error": "Username already exists"}, 400
        # Create new user
        user = User(username=username)
        user._password_hash = generate_password_hash(password).decode('utf-8')
        db.session.add(user)
        db.session.commit()
        return {"message": "User created"}, 201

class LoginResource(Resource):
    """Handle user login"""
    def post(self):
        # Get login data
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')
        # Find user
        user = User.query.filter_by(username=username).first()
        # Check password
        if not user or not check_password_hash(user._password_hash, password):
            return {"error": "Invalid credentials"}, 401
        # Create token
        access_token = create_access_token(identity=user.id)
        return {"access_token": access_token}, 200

class MeResource(Resource):
    """Get current user info"""
    @jwt_required()
    def get(self):
        # Get user id from token
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        if not user:
            return {"error": "User not found"}, 404
        return {"id": user.id, "username": user.username}, 200