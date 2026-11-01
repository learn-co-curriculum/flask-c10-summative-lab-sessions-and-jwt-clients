from flask import Flask, request
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required
from config import Config
from extension import db, migrate, jwt, bcrypt
from models import User, Task

app = Flask(__name__)

app.config.from_object(Config)

db.init_app(app)
migrate.init_app(app, db)
jwt.init_app(app)
bcrypt.init_app(app)


@app.route("/")
def home():
    return {"message": "Task Management API is running!"}


@app.route("/signup", methods=["POST"])
def signup():
    data = request.get_json()

    username = data.get("username")
    password = data.get("password")
    password_confirmation = data.get("password_confirmation")

    if not username or not password or not password_confirmation:
        return {"errors": ["All fields are required"]}, 400

    if password != password_confirmation:
        return {"errors": ["Passwords do not match"]}, 400

    existing_user = User.query.filter_by(username=username).first()

    if existing_user:
        return {"errors": ["Username already exists"]}, 422

    password_hash = bcrypt.generate_password_hash(password).decode("utf-8")

    new_user = User(
        username=username,
        password_hash=password_hash
    )

    db.session.add(new_user)
    db.session.commit()

    access_token = create_access_token(identity=str(new_user.id))

    return {
        "token": access_token,
        "user": {
            "id": new_user.id,
            "username": new_user.username
        }
    }, 201


@app.route("/login", methods=["POST"])
def login():
    data = request.get_json() or {}

    username = data.get("username")
    password = data.get("password")

    if not username or not password:
        return {"errors": ["Username and password are required"]}, 400

    user = User.query.filter_by(username=username).first()

    if not user:
        return {"errors": ["User not found"]}, 404

    if not bcrypt.check_password_hash(user.password_hash, password):
        return {"errors": ["Invalid password"]}, 401

    access_token = create_access_token(identity=str(user.id))

    return {
        "token": access_token,
        "user": {
            "id": user.id,
            "username": user.username
        }
    }, 200


@app.route("/me", methods=["GET"])
@jwt_required()
def me():
    user_id = get_jwt_identity()

    user = db.session.get(User, int(user_id))

    if not user:
        return {"errors": ["User not found"]}, 404

    return {
        "id": user.id,
        "username": user.username
    }, 200


@app.route("/tasks", methods=["GET"])
@jwt_required()
def get_tasks():
    user_id = get_jwt_identity()

    tasks = Task.query.filter_by(user_id=user_id).all()

    return {
        "tasks": [
            {
                "id": task.id,
                "title": task.title,
                "description": task.description,
                "completed": task.completed,
                "user_id": task.user_id
            }
            for task in tasks
        ]
    }, 200


@app.route("/tasks", methods=["POST"])
@jwt_required()
def create_task():
    data = request.get_json() or {}

    title = data.get("title")
    description = data.get("description")

    if not title:
        return {"errors": ["Title is required"]}, 400

    user_id = get_jwt_identity()

    new_task = Task(
        title=title,
        description=description,
        user_id=user_id
    )

    db.session.add(new_task)
    db.session.commit()

    return {
        "id": new_task.id,
        "title": new_task.title,
        "description": new_task.description,
        "completed": new_task.completed,
        "user_id": new_task.user_id
    }, 201


@app.route("/tasks/<int:id>", methods=["GET"])
@jwt_required()
def get_task(id):
    user_id = get_jwt_identity()

    task = Task.query.filter_by(
        id=id,
        user_id=user_id
    ).first()

    if not task:
        return {"errors": ["Task not found"]}, 404

    return {
        "id": task.id,
        "title": task.title,
        "description": task.description,
        "completed": task.completed,
        "user_id": task.user_id
    }, 200