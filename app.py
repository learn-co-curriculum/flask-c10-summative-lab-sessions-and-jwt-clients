import os

from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_jwt_extended import (
    JWTManager,
    create_access_token,
    get_jwt_identity,
    jwt_required,
)
from flask_migrate import Migrate
from flask_restful import Api
from sqlalchemy import text

from models import Note, User, bcrypt, db


app = Flask(__name__)

database_url = os.environ.get("DATABASE_URL", "sqlite:///productivity_app.db")
if database_url.startswith("postgres://"):
    database_url = database_url.replace("postgres://", "postgresql://", 1)
app.config["SQLALCHEMY_DATABASE_URI"] = database_url
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["JWT_SECRET_KEY"] = os.environ.get("JWT_SECRET_KEY", "dev-secret-key")
app.config["JSON_SORT_KEYS"] = False

api = Api(app)
db.init_app(app)

cors_origins = os.environ.get("CORS_ORIGINS", "*")
if cors_origins != "*":
    cors_origins = [origin.strip() for origin in cors_origins.split(",")]
CORS(app, resources={r"/*": {"origins": cors_origins}})

VALID_CATEGORIES = ["Notes", "Tasks", "Workouts", "Journal"]


def normalize_category(value):
    category = (value or "Notes").strip()
    return category if category in VALID_CATEGORIES else "Notes"


def ensure_note_category_column():
    with app.app_context():
        inspector = db.inspect(db.engine)
        if "notes" not in inspector.get_table_names():
            db.create_all()
            return

        columns = [column["name"] for column in inspector.get_columns("notes")]
        if "category" not in columns:
            db.session.execute(
                text("ALTER TABLE notes ADD COLUMN category VARCHAR(50) NOT NULL DEFAULT 'Notes'")
            )
            db.session.commit()


def seed_demo_data():
    with app.app_context():
        if Note.query.first() is not None:
            return

        demo_user = User.query.filter_by(username="demo").first()
        if demo_user is None:
            demo_user = User(username="demo")
            demo_user.password = "password123"
            db.session.add(demo_user)
            db.session.flush()

        if Note.query.filter_by(user_id=demo_user.id).count() == 0:
            demo_notes = [
                Note(
                    title="Morning plan",
                    content="Review priorities and set the top three goals for the day.",
                    category="Notes",
                    user_id=demo_user.id,
                ),
                Note(
                    title="Strength workout",
                    content="30-minute circuit: squats, lunges, rows, and core work.",
                    category="Workouts",
                    user_id=demo_user.id,
                ),
                Note(
                    title="Deep work block",
                    content="Finish the design pass and clean up the final API wiring before lunch.",
                    category="Tasks",
                    user_id=demo_user.id,
                ),
                Note(
                    title="Journal reflection",
                    content="The improved layout feels calmer and easier to read today.",
                    category="Journal",
                    user_id=demo_user.id,
                ),
            ]
            db.session.add_all(demo_notes)
            db.session.commit()


migrate = Migrate(app, db)
jwt = JWTManager(app)
with app.app_context():
    db.create_all()
    ensure_note_category_column()
    seed_demo_data()


@app.get("/")
def home():
    return jsonify(message="Productivity API is running")


def current_user():
    user_id = get_jwt_identity()
    if user_id is None:
        return None
    return User.query.get(int(user_id))


@app.post("/signup")
def signup():
    data = request.get_json(silent=True) or {}
    username = (data.get("username") or "").strip()
    password = data.get("password")
    password_confirmation = data.get("password_confirmation")

    if not username or not password or not password_confirmation:
        return jsonify({"errors": ["Username and password are required."]}), 400

    if password != password_confirmation:
        return jsonify({"errors": ["Passwords do not match."]}), 400

    if User.query.filter_by(username=username).first():
        return jsonify({"errors": ["Username already exists."]}), 409

    user = User(username=username)
    user.password = password
    db.session.add(user)
    db.session.commit()

    token = create_access_token(identity=str(user.id))
    return jsonify({"token": token, "user": user.serialize()}), 201


@app.post("/login")
def login():
    data = request.get_json(silent=True) or {}
    username = (data.get("username") or "").strip()
    password = data.get("password")

    if not username or not password:
        return jsonify({"errors": ["Username and password are required."]}), 400

    user = User.query.filter_by(username=username).first()
    if not user or not user.check_password(password):
        return jsonify({"errors": ["Invalid username or password."]}), 401

    token = create_access_token(identity=str(user.id))
    return jsonify({"token": token, "user": user.serialize()})


@app.get("/me")
@jwt_required()
def me():
    user = current_user()
    if not user:
        return jsonify({"error": "User not found."}), 404
    return jsonify(user.serialize())


@app.get("/notes")
@jwt_required()
def get_notes():
    user = current_user()
    page = request.args.get("page", default=1, type=int)
    per_page = request.args.get("per_page", default=10, type=int)
    category_filter = request.args.get("category")

    if page < 1:
        page = 1
    if per_page < 1:
        per_page = 10

    query = Note.query.filter_by(user_id=user.id)
    if category_filter:
        query = query.filter_by(category=normalize_category(category_filter))

    pagination = (
        query.order_by(Note.id.desc()).paginate(page=page, per_page=per_page, error_out=False)
    )

    return jsonify(
        {
            "items": [note.serialize() for note in pagination.items],
            "page": pagination.page,
            "per_page": pagination.per_page,
            "total": pagination.total,
            "pages": pagination.pages,
        }
    )


@app.post("/notes")
@jwt_required()
def create_note():
    user = current_user()
    data = request.get_json(silent=True) or {}
    title = (data.get("title") or "").strip()
    content = (data.get("content") or "").strip()
    category = normalize_category(data.get("category"))

    if not title or not content:
        return jsonify({"errors": ["Title and content are required."]}), 400

    note = Note(title=title, content=content, category=category, user_id=user.id)
    db.session.add(note)
    db.session.commit()
    return jsonify(note.serialize()), 201


@app.patch("/notes/<int:note_id>")
@jwt_required()
def update_note(note_id):
    user = current_user()
    note = Note.query.filter_by(id=note_id).first()

    if not note:
        return jsonify({"error": "Note not found."}), 404
    if note.user_id != user.id:
        return jsonify({"error": "You are not allowed to modify this note."}), 403

    data = request.get_json(silent=True) or {}
    if "title" in data:
        title = (data.get("title") or "").strip()
        if not title:
            return jsonify({"errors": ["Title cannot be empty."]}), 400
        note.title = title
    if "content" in data:
        content = (data.get("content") or "").strip()
        if not content:
            return jsonify({"errors": ["Content cannot be empty."]}), 400
        note.content = content
    if "category" in data:
        note.category = normalize_category(data.get("category"))

    db.session.commit()
    return jsonify(note.serialize())


@app.delete("/notes/<int:note_id>")
@jwt_required()
def delete_note(note_id):
    user = current_user()
    note = Note.query.filter_by(id=note_id).first()

    if not note:
        return jsonify({"error": "Note not found."}), 404
    if note.user_id != user.id:
        return jsonify({"error": "You are not allowed to delete this note."}), 403

    db.session.delete(note)
    db.session.commit()
    return jsonify({"message": "Note deleted successfully."})


if __name__ == "__main__":
    app.run(debug=True)
