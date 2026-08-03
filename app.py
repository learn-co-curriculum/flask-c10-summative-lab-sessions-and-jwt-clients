import os
from flask import Flask, jsonify, request
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager, create_access_token, get_jwt_identity, jwt_required
from flask_migrate import Migrate
from flask_restful import Api, Resource
from flask_sqlalchemy import SQLAlchemy

from models import Note, User, db


bcrypt = Bcrypt()
migrate = Migrate()
jwt = JWTManager()


def create_app():
    """Create and configure the Flask application for the notes API."""
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL", "sqlite:///app.db")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["JWT_SECRET_KEY"] = os.environ.get("JWT_SECRET_KEY", "a-very-secure-development-secret-key")
    app.config["JSON_SORT_KEYS"] = False

    db.init_app(app)
    bcrypt.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)

    api = Api(app)
    api.add_resource(NoteListResource, "/notes")
    api.add_resource(NoteDetailResource, "/notes/<int:note_id>")

    @app.route("/signup", methods=["POST"])
    def signup():
        data = request.get_json(silent=True) or {}
        username = (data.get("username") or "").strip()
        password = data.get("password")
        password_confirmation = data.get("password_confirmation")

        if not username or not password:
            return jsonify({"errors": ["username and password are required"]}), 400

        if password != password_confirmation:
            return jsonify({"errors": ["passwords do not match"]}), 400

        if User.query.filter_by(username=username).first():
            return jsonify({"errors": ["that username is already taken"]}), 400

        user = User(username=username, password=password)
        db.session.add(user)
        db.session.commit()

        token = create_access_token(identity=str(user.id))
        return jsonify({"token": token, "user": user.to_dict()}), 201

    @app.route("/login", methods=["POST"])
    def login():
        data = request.get_json(silent=True) or {}
        username = (data.get("username") or "").strip()
        password = data.get("password")

        user = User.query.filter_by(username=username).first()
        if not user or not user.check_password(password):
            return jsonify({"errors": ["invalid username or password"]}), 401

        token = create_access_token(identity=str(user.id))
        return jsonify({"token": token, "user": user.to_dict()}), 200

    @app.route("/me", methods=["GET"])
    @jwt_required()
    def me():
        user = User.query.get(int(get_jwt_identity()))
        if not user:
            return jsonify({"errors": ["user not found"]}), 404
        return jsonify(user.to_dict()), 200

    @app.route("/health", methods=["GET"])
    def health():
        return jsonify({"status": "ok"}), 200

    return app


class NoteListResource(Resource):
    @jwt_required()
    def get(self):
        user_id = int(get_jwt_identity())
        page = request.args.get("page", default=1, type=int)
        per_page = request.args.get("per_page", default=10, type=int)
        page = max(page, 1)
        per_page = max(min(per_page, 25), 1)

        pagination = (
            Note.query.filter_by(user_id=user_id)
            .order_by(Note.created_at.desc())
            .paginate(page=page, per_page=per_page, error_out=False)
        )

        return {
            "notes": [note.to_dict() for note in pagination.items],
            "pagination": {
                "page": page,
                "per_page": per_page,
                "total_pages": pagination.pages,
                "total_items": pagination.total,
            },
        }, 200

    @jwt_required()
    def post(self):
        user_id = int(get_jwt_identity())
        data = request.get_json(silent=True) or {}
        title = (data.get("title") or "").strip()
        content = (data.get("content") or "").strip()

        if not title or not content:
            return {"errors": ["title and content are required"]}, 400

        note = Note(title=title, content=content, user_id=user_id)
        db.session.add(note)
        db.session.commit()
        return note.to_dict(), 201


class NoteDetailResource(Resource):
    @jwt_required()
    def patch(self, note_id):
        user_id = int(get_jwt_identity())
        note = Note.query.filter_by(id=note_id, user_id=user_id).first()
        if not note:
            return {"errors": ["note not found"]}, 404

        data = request.get_json(silent=True) or {}
        if "title" in data:
            title = (data.get("title") or "").strip()
            if not title:
                return {"errors": ["title cannot be empty"]}, 400
            note.title = title
        if "content" in data:
            content = (data.get("content") or "").strip()
            if not content:
                return {"errors": ["content cannot be empty"]}, 400
            note.content = content

        db.session.commit()
        return note.to_dict(), 200

    @jwt_required()
    def delete(self, note_id):
        user_id = int(get_jwt_identity())
        note = Note.query.filter_by(id=note_id, user_id=user_id).first()
        if not note:
            return {"errors": ["note not found"]}, 404

        db.session.delete(note)
        db.session.commit()
        return {}, 204


app = create_app()


if __name__ == "__main__":
    app.run(port=5555, debug=True)
