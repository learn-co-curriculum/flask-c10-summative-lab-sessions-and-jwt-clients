from flask_restful import Resource
from flask import request
from flask_login import login_user, logout_user, login_required, current_user
from models import User, db
from flask_bcrypt import check_password_hash

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
        login_user(user)
        return {"id": user.id, "username": user.username}, 201

class LoginResource(Resource):
    def post(self):
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')
        user = User.query.filter_by(username=username).first()
        if not user or not check_password_hash(user._password_hash, password):
            return {"error": "Invalid credentials"}, 401
        login_user(user)
        return {"id": user.id, "username": user.username}, 200

class LogoutResource(Resource):
    @login_required
    def post(self):
        logout_user()
        return {"message": "Logged out"}, 200

class MeResource(Resource):
    @login_required
    def get(self):
        return {"id": current_user.id, "username": current_user.username}, 200