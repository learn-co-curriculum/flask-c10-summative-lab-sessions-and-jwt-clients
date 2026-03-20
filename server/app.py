from flask import Flask, jsonify, request
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity

from config import Config
from models import db, bcrypt, User, Note  


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Init extensions
    db.init_app(app)
    bcrypt.init_app(app)
    Migrate(app, db)
    JWTManager(app)

    @app.get("/")
    def home():
        return jsonify({"message": "API is running"}), 200
    
    @app.post("/signup")
    def signup():
        """Register a new user and return an access token."""
        data = request.get_json() or {}

        username = (data.get("username") or "").strip()
        password = data.get("password") or ""

        if not username or not password:
            return jsonify({"errors": ["Username and password are required."]}), 400

        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            return jsonify({"errors": ["Username is already taken."]}), 409

        user = User(username=username)
        user.set_password(password)

        db.session.add(user)
        db.session.commit()

        token = create_access_token(identity=user.id)

        return jsonify({
            "token": token,
            "user": {"id": user.id, "username": user.username}
        }), 201

    @app.post("/login")
    def login():
        """Log in a user and return an access token."""
        data = request.get_json() or {}

        username = (data.get("username") or "").strip()
        password = data.get("password") or ""

        user = User.query.filter_by(username=username).first()

        if user is None or not user.check_password(password):
            return jsonify({"errors": ["Invalid username or password."]}), 401

        token = create_access_token(identity=user.id)

        return jsonify({
            "token": token,
            "user": {"id": user.id, "username": user.username}
        }), 200
    
    @app.get("/me")
    @jwt_required()
    def me():
        # Get the current user's id from the JWT token
        user_id = get_jwt_identity()

        # Fetch the user from the database
        user = User.query.get(user_id)

        if not user:
            return jsonify({"error": "User not found."}), 404

        return jsonify({
            "id": user.id,
            "username": user.username
        }), 200
    
    @app.get("/notes")
    @jwt_required()
    def get_notes():
        """Return a paginated list of notes for the logged-in user."""
        user_id = get_jwt_identity()

        # Read pagination params from the query string:
        # /notes?page=1&per_page=10
        page = request.args.get("page", 1, type=int)
        per_page = request.args.get("per_page", 10, type=int)

        # Basic safety limits 
        if page < 1:
            page = 1
        if per_page < 1:
            per_page = 10
        if per_page > 50:
            per_page = 50

        pagination = (
            Note.query
            .filter_by(user_id=user_id)
            .order_by(Note.id.asc())
            .paginate(page=page, per_page=per_page, error_out=False)
        )

        notes_data = [
            {"id": n.id, "title": n.title, "content": n.content}
            for n in pagination.items
        ]

        return jsonify({
            "notes": notes_data,
            "page": pagination.page,
            "per_page": pagination.per_page,
            "total": pagination.total,
            "pages": pagination.pages,
        }), 200

    @app.get("/notes/<int:id>")
    @jwt_required()
    def get_note(id):
        user_id = get_jwt_identity()

        note = Note.query.filter_by(id=id, user_id=user_id).first()
        if not note:
            return jsonify({"error": "Note not found"}), 404

        return jsonify({
            "id": note.id,
            "title": note.title,
            "content": note.content
        }), 200
    
    @app.post("/notes")
    @jwt_required()
    def create_note():
        user_id = get_jwt_identity()
        data = request.get_json() or {}

        title = (data.get("title") or "").strip()
        content = (data.get("content") or "").strip()

        if not title or not content:
            return jsonify({"errors": ["Title and content are required."]}), 400

        note = Note(title=title, content=content, user_id=user_id)
        db.session.add(note)
        db.session.commit()

        return jsonify({
            "id": note.id,
            "title": note.title,
            "content": note.content
        }), 201
    

    @app.patch("/notes/<int:id>")
    @jwt_required()
    def update_note(id):
        user_id = get_jwt_identity()
        note = Note.query.filter_by(id=id, user_id=user_id).first()

        if not note:
            return jsonify({"error": "Note not found"}), 404

        data = request.get_json() or {}

        title = data.get("title")
        content = data.get("content")

        if title is not None:
            title = title.strip()
            if title == "":
                return jsonify({"errors": ["Title cannot be empty."]}), 400
        note.title = title

        if content is not None:
            content = content.strip()
            if content == "":
                return jsonify({"errors": ["Content cannot be empty."]}), 400
            note.content = content

        db.session.commit()

        return jsonify({
             "id": note.id,
             "title": note.title,
             "content": note.content
        }), 200
    @app.delete("/notes/<int:id>")
    @jwt_required()
    def delete_note(id):
        user_id = get_jwt_identity()
        note = Note.query.filter_by(id=id, user_id=user_id).first()

        if not note:
            return jsonify({"error": "Note not found"}), 404

        db.session.delete(note)
        db.session.commit()

        return jsonify({"message": "Note deleted"}), 200
    
    return app


app = create_app()

if __name__ == "__main__":
    app.run(port=5555, debug=True)