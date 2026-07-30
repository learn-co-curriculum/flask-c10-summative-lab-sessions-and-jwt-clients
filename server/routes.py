from flask import request, session, jsonify

from extensions import db
from models import User


def register_routes(app):

    @app.post("/signup")
    def signup():
        data = request.get_json()

        username = data.get("username")
        password = data.get("password")
        password_confirmation = data.get("password_confirmation")

        if password != password_confirmation:
            return jsonify({"error": "Passwords do not match."}), 400

        if User.query.filter_by(username=username).first():
            return jsonify({"error": "Username already exists."}), 400

        try:
            user = User(username=username)
            user.password_hash = password

            db.session.add(user)
            db.session.commit()

            session["user_id"] = user.id

            return jsonify(user.to_dict()), 201

        except ValueError as e:
            db.session.rollback()
            return jsonify({"error": str(e)}), 400