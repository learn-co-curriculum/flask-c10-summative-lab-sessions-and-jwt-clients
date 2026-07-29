from flask import Flask, jsonify, request
from flask_jwt_extended import JWTManager, create_access_token, get_jwt_identity, jwt_required
from flask_migrate import Migrate
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError

from config import Config
from models import Note, User, bcrypt, db


def error(message, status):
    return jsonify({"error": message}), status


def request_json():
    data = request.get_json(silent=True)
    if not isinstance(data, dict):
        return None
    return data


def get_owned_note(note_id, user_id):
    # Query by both fields so another user's note is never disclosed.
    return db.session.scalar(
        select(Note).where(Note.id == note_id, Note.user_id == user_id)
    )


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    bcrypt.init_app(app)
    Migrate(app, db)
    jwt = JWTManager(app)

    @jwt.unauthorized_loader
    def missing_token(reason):
        return error("Authorization token is required.", 401)

    @jwt.invalid_token_loader
    def invalid_token(reason):
        return error("Authorization token is invalid.", 401)

    @jwt.expired_token_loader
    def expired_token(jwt_header, jwt_payload):
        return error("Authorization token has expired.", 401)

    @app.errorhandler(404)
    def not_found(_):
        return error("Resource not found.", 404)

    @app.post("/register")
    def register():
        data = request_json()
        if not data:
            return error("A JSON request body is required.", 400)

        username = data.get("username")
        email = data.get("email")
        password = data.get("password")
        if not all(isinstance(value, str) for value in (username, email, password)):
            return error("username, email, and password are required.", 400)
        username = username.strip()
        email = email.strip().lower()
        if not username or not email or not password:
            return error("username, email, and password are required.", 400)
        if len(username) > 80 or len(email) > 120 or len(password) < 8:
            return error("Use a valid username/email and a password of at least 8 characters.", 400)
        if db.session.scalar(select(User).where(User.username == username)):
            return error("Username is already in use.", 400)
        if db.session.scalar(select(User).where(User.email == email)):
            return error("Email is already in use.", 400)

        user = User(username=username, email=email)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        return jsonify({"user": user.to_dict()}), 201

    @app.post("/login")
    def login():
        data = request_json()
        if not data:
            return error("A JSON request body is required.", 400)

        username = data.get("username")
        password = data.get("password")
        if not isinstance(username, str) or not isinstance(password, str):
            return error("username and password are required.", 400)
        username = username.strip()
        if not username or not password:
            return error("username and password are required.", 400)

        user = db.session.scalar(select(User).where(User.username == username))
        if not user or not user.check_password(password):
            return error("Invalid username or password.", 401)
        return jsonify({"access_token": create_access_token(identity=str(user.id)), "user": user.to_dict()}), 200

    @app.get("/me")
    @jwt_required()
    def current_user():
        user = db.session.get(User, int(get_jwt_identity()))
        if not user:
            return error("Resource not found.", 404)
        return jsonify({"user": user.to_dict()}), 200

    @app.get("/notes")
    @jwt_required()
    def list_notes():
        try:
            page = int(request.args.get("page", 1))
            per_page = int(request.args.get("per_page", 10))
        except ValueError:
            return error("page and per_page must be integers.", 400)
        if page < 1 or not 1 <= per_page <= 100:
            return error("page must be positive and per_page must be between 1 and 100.", 400)

        user_id = int(get_jwt_identity())
        pagination = db.paginate(
            select(Note).where(Note.user_id == user_id).order_by(Note.created_at.desc()),
            page=page,
            per_page=per_page,
            error_out=False,
        )
        return jsonify({
            "notes": [note.to_dict() for note in pagination.items],
            "pagination": {"total": pagination.total, "page": page, "pages": pagination.pages},
        }), 200

    @app.get("/notes/<int:note_id>")
    @jwt_required()
    def get_note(note_id):
        note = get_owned_note(note_id, int(get_jwt_identity()))
        if not note:
            return error("Resource not found.", 404)
        return jsonify({"note": note.to_dict()}), 200

    @app.post("/notes")
    @jwt_required()
    def create_note():
        data = request_json()
        if not data:
            return error("A JSON request body is required.", 400)
        raw_title = data.get("title")
        content = data.get("content", "")
        if not isinstance(raw_title, str) or not isinstance(content, str):
            return error("title is required and content must be a string.", 400)
        title = raw_title.strip()
        if not title:
            return error("title is required and content must be a string.", 400)
        if len(title) > 255:
            return error("title must be 255 characters or fewer.", 400)

        note = Note(title=title, content=content, user_id=int(get_jwt_identity()))
        db.session.add(note)
        db.session.commit()
        return jsonify({"note": note.to_dict()}), 201

    @app.patch("/notes/<int:note_id>")
    @jwt_required()
    def update_note(note_id):
        data = request_json()
        if not data or not {"title", "content"}.intersection(data):
            return error("Provide title and/or content in a JSON request body.", 400)

        note = get_owned_note(note_id, int(get_jwt_identity()))
        if not note:
            return error("Resource not found.", 404)
        if "title" in data:
            if not isinstance(data["title"], str) or not data["title"].strip() or len(data["title"].strip()) > 255:
                return error("title must be a non-empty string of 255 characters or fewer.", 400)
            note.title = data["title"].strip()
        if "content" in data:
            if not isinstance(data["content"], str):
                return error("content must be a string.", 400)
            note.content = data["content"]
        db.session.commit()
        return jsonify({"note": note.to_dict()}), 200

    @app.delete("/notes/<int:note_id>")
    @jwt_required()
    def delete_note(note_id):
        note = get_owned_note(note_id, int(get_jwt_identity()))
        if not note:
            return error("Resource not found.", 404)
        db.session.delete(note)
        db.session.commit()
        return "", 204

    @app.errorhandler(IntegrityError)
    def integrity_error(_):
        db.session.rollback()
        return error("Could not save the requested resource.", 400)

    return app


app = create_app()
