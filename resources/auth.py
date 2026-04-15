from flask_restful import Resource
from flask import request, jsonify
import jwt
from datetime import datetime, timedelta
from models import User, db
from flask_bcrypt import check_password_hash
from resources.config import Config
from functools import wraps

def jwt_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        auth_header = request.headers.get('Authorization')
        if not auth_header:
            return {"error": "Token missing"}, 401
        try:
            token = auth_header.split(" ")[1] if " " in auth_header else auth_header
            payload = jwt.decode(token, Config.SECRET_KEY, algorithms=['HS256'])
            request.user = User.query.get(payload['user_id'])
            if not request.user:
                return {"error": "User not found"}, 401
        except jwt.ExpiredSignatureError:
            return {"error": "Token expired"}, 401
        except jwt.InvalidTokenError:
            return {"error": "Invalid token"}, 401
        return f(*args, **kwargs)
    return decorated_function

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
        user.password_hash = password
        db.session.add(user)
        db.session.commit()
        token = jwt.encode({
            'user_id': user.id,
            'exp': datetime.utcnow() + timedelta(hours=24)
        }, Config.SECRET_KEY, algorithm='HS256')
        return {"token": token, "user": {"id": user.id, "username": user.username}}, 201

class LoginResource(Resource):
    def post(self):
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')
        user = User.query.filter_by(username=username).first()
        if not user or not check_password_hash(user._password_hash, password):
            return {"error": "Invalid credentials"}, 401
        token = jwt.encode({
            'user_id': user.id,
            'exp': datetime.utcnow() + timedelta(hours=24)
        }, Config.SECRET_KEY, algorithm='HS256')
        return {"token": token, "user": {"id": user.id, "username": user.username}}, 200

class LogoutResource(Resource):
    def post(self):
        return {"message": "Logged out"}, 200

class MeResource(Resource):
    def get(self):
        auth_header = request.headers.get('Authorization')
        if not auth_header:
            return {"error": "Token missing"}, 401
        try:
            token = auth_header.split(" ")[1] if " " in auth_header else auth_header
            payload = jwt.decode(token, Config.SECRET_KEY, algorithms=['HS256'])
            user = User.query.get(payload['user_id'])
            if not user:
                return {"error": "User not found"}, 401
            return {"id": user.id, "username": user.username}, 200
        except jwt.ExpiredSignatureError:
            return {"error": "Token expired"}, 401
        except jwt.InvalidTokenError:
            return {"error": "Invalid token"}, 401