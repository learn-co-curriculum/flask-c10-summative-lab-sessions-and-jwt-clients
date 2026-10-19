
import os
from flask import Flask, request, session
from flask_migrate import Migrate
from models import db, bcrypt, User
from models import db, bcrypt, User, Task

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///taskflow.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "local-dev-key")

db.init_app(app)
bcrypt.init_app(app)
migrate = Migrate(app, db)


@app.route("/")
def home():
    return {"message": "Welcome to TaskFlow API"}, 200

 
@app.route("/signup", methods=["POST"])
def signup():
    data = request.get_json(silent=True) or {}

    username = data.get("username")
    password = data.get("password")
    confirmation = data.get("password_confirmation")

    if not isinstance(username, str) or not username.strip():
        return {"errors": ["Username is required"]}, 400

    if not isinstance(password, str) or not password:
        return {"errors": ["Password is required"]}, 400

    if password != confirmation:
        return {"errors": ["Passwords do not match"]}, 400

    username = username.strip()

    if User.query.filter_by(username=username).first():
        return {"errors": ["Username already exists"]}, 409

    user = User(username=username)
    user.set_password(password)

    db.session.add(user)
    db.session.commit()

    session.clear()
    session["user_id"] = user.id

    return user.to_dict(), 201


@app.route("/login", methods=["POST"])
def login():
    data = request.get_json(silent=True) or {}
    username = data.get("username")
    password = data.get("password")

    if not isinstance(username, str) or not isinstance(password, str):
        return {"errors": ["Invalid username or password"]}, 401
    user = User.query.filter_by(username=username).first()

    if not user or not user.check_password(password):
     return {"errors": ["Invalid username or password"]}, 401
    session.clear()
    session["user_id"] = user.id

    return user.to_dict(), 200

@app.route("/check_session", methods=["GET"])
def check_session():
    user_id = session.get("user_id")

    if not user_id:
        return {"error": "Not authorized"}, 401

    user = db.session.get(User, user_id)

    if not user:
        session.clear()
        return {"error": "Not authorized"}, 401

    return user.to_dict(), 200

@app.route("/logout", methods=["DELETE"])
def logout():
    session.clear()
    return {}, 204

@app.route("/tasks", methods=["GET"])
def get_tasks():
    user_id = session.get("user_id")

    if not user_id:
        return {"error": "Not authorized"}, 401

    page = request.args.get("page", 1, type=int)
    per_page = 5

    if page < 1:
        return {"error": "Invalid page"}, 400

    tasks = Task.query.filter_by(user_id=user_id).order_by(
        Task.id.desc()
    ).paginate(page=page, per_page=per_page, error_out=False)

    return {
        "tasks": [task.to_dict() for task in tasks.items],
        "page": page,
        "total": tasks.total,
        "pages": tasks.pages
    }, 200

@app.route("/tasks", methods=["POST"])
def add_task():
    user_id = session.get("user_id")

    if not user_id:
        return {"error": "Not authorized"}, 401

    data = request.get_json(silent=True) or {}
    title = data.get("title")
    description = data.get("description", "")

    if not isinstance(title, str) or not title.strip():
        return {"error": "Title is required"}, 400

    if not isinstance(description, str):
        return {"error": "Invalid description"}, 400

    task = Task(
        title=title.strip(),
        description=description,
        user_id=user_id
    )

    db.session.add(task)
    db.session.commit()

    return task.to_dict(), 201

@app.route("/tasks/<int:id>", methods=["GET"])
def get_task(id):
    user_id = session.get("user_id")

    if not user_id:
        return {"error": "Not authorized"}, 401

    task = Task.query.filter_by(id=id, user_id=user_id).first()

    if not task:
        return {"error": "Task not found"}, 404

    return task.to_dict(), 200


@app.route("/tasks/<int:id>", methods=["PATCH"])
def update_task(id):
    user_id = session.get("user_id")

    if not user_id:
        return {"error": "Not authorized"}, 401

    task = Task.query.filter_by(id=id, user_id=user_id).first()

    if not task:
        return {"error": "Task not found"}, 404

    data = request.get_json(silent=True) or {}

    if "title" in data:
        if not isinstance(data["title"], str) or not data["title"].strip():
            return {"error": "Invalid title"}, 400
        task.title = data["title"].strip()

    if "description" in data:
        if not isinstance(data["description"], str):
            return {"error": "Invalid description"}, 400
        task.description = data["description"]

    if "completed" in data:
        if not isinstance(data["completed"], bool):
            return {"error": "Invalid completed value"}, 400
        task.completed = data["completed"]

    db.session.commit()

    return task.to_dict(), 200

@app.route("/tasks/<int:id>", methods=["DELETE"])
def delete_task(id):
    user_id = session.get("user_id")

    if not user_id:
        return {"error": "Not authorized"}, 401

    task = Task.query.filter_by(id=id, user_id=user_id).first()

    if not task:
        return {"error": "Task not found"}, 404

    db.session.delete(task)
    db.session.commit()

    return "", 204

if __name__ == "__main__":
    app.run(debug=True)
