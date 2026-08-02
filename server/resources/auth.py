from flask import request
from flask_restful import Resource
from flask_jwt_extended import (
    create_access_token,
    jwt_required,
    get_jwt_identity
)

from config import db
from models import User


class Signup(Resource):
    def post(self):
        data = request.get_json()

        username = data.get("username")
        email = data.get("email")
        password = data.get("password")

        if User.query.filter_by(email=email).first():
            return {"error": "Email already exists"}, 400

        user = User(
            username=username,
            email=email
        )

        user.password = password

        db.session.add(user)
        db.session.commit()

        return user.to_dict(), 201


class Login(Resource):
    def post(self):
        data = request.get_json()

        email = data.get("email")
        password = data.get("password")

        user = User.query.filter_by(email=email).first()

        if not user:
            return {"error": "Invalid email or password"}, 401

        if not user.authenticate(password):
            return {"error": "Invalid email or password"}, 401

        access_token = create_access_token(identity=user.id)

        return {
            "message": "Login successful",
            "access_token": access_token,
            "user": user.to_dict()
        }, 200
class Me(Resource):
    @jwt_required()
    def get(self):
        user_id = get_jwt_identity()

        user = User.query.get(user_id)

        if not user:
            return {"error": "User not found"}, 404

        return user.to_dict(), 200