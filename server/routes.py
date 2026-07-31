from flask import request, jsonify
from flask_jwt_extended import (
    create_access_token,
    jwt_required,
    get_jwt_identity,
)

from extensions import db
from models import User


def register_routes(app):

    @app.post("/signup")
    def signup():
        data = request.get_json()

        if not data:
            return jsonify({"error": "Request body must be JSON"}), 400

        username = data.get("username")
        password = data.get("password")
        password_confirmation = data.get("password_confirmation")

        if not username or not password or not password_confirmation:
            return jsonify({
                "error": "Username, password and password_confirmation are required"
            }), 400

        if password != password_confirmation:
            return jsonify({
                "error": "Passwords do not match"
            }), 400

        if User.query.filter_by(username=username).first():
            return jsonify({
                "error": "Username already exists"
            }), 400

        try:
            user = User(username=username)
            user.password_hash = password

            db.session.add(user)
            db.session.commit()

            # Create JWT token
            token = create_access_token(identity=user.id)

            return jsonify({
                "token": token,
                "user": user.to_dict()
            }), 201

        except ValueError as e:
            db.session.rollback()
            return jsonify({"error": str(e)}), 400


    @app.post("/login")
    def login():
        data = request.get_json()

        if not data:
            return jsonify({"error": "Request body must be JSON"}), 400

        username = data.get("username")
        password = data.get("password")

        if not username or not password:
            return jsonify({
                "error": "Username and password are required"
            }), 400

        user = User.query.filter_by(username=username).first()

        if user is None or not user.authenticate(password):
            return jsonify({
                "error": "Invalid username or password"
            }), 401

        # Create JWT token
        token = create_access_token(identity=str(user.id))

        return jsonify({
            "token": token,
            "user": user.to_dict()
        }), 201


        token = create_access_token(identity=str(user.id))

        return jsonify({
            "token": token,
            "user": user.to_dict()
        }), 200


    @app.get("/me")
    @jwt_required()
    def me():

        user_id = int(get_jwt_identity())

        user = db.session.get(User, user_id)

        if user is None:
            return jsonify({"error": "User not found"}), 404


        return jsonify(user.to_dict()), 200