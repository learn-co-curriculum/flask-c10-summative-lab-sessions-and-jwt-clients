from flask_restful import Resource
from flask import request
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from models import User, db
from flask_bcrypt import generate_password_hash, check_password_hash

class SignupResource(Resource):
    def post(self):
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')
        if not username or not password:
            return {"error": "Username and password required"}, 400
        if User.query.filter_by(username=username).first():
            return {"error": "Username already exists"}, 400
        user = User(username=username)
        user._password_hash = generate_password_hash(password).decode('utf-8')
        db.session.add(user)
        db.session.commit()
        return {"message": "User created"}, 201

class LoginResource(Resource):
    def post(self):
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')
        user = User.query.filter_by(username=username).first()
        if not user or not check_password_hash(user._password_hash, password):
            return {"error": "Invalid credentials"}, 401
        access_token = create_access_token(identity=user.id)
        return {"access_token": access_token}, 200

class MeResource(Resource):
    @jwt_required()
    def get(self):
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        if not user:
            return {"error": "User not found"}, 404
        return {"id": user.id, "username": user.username}, 200