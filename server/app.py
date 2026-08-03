from flask import Flask, request
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from schemas import user_schema, task_schema, tasks_schema

from config import Config, db, bcrypt, migrate, jwt

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)
bcrypt.init_app(app)
migrate.init_app(app, db)
jwt.init_app(app)

from models import User, Task


@app.route("/")
def home():
    return {"message": "Productivity API is running!"}

@app.post("/signup")
def signup():
    data = request.get_json()

    username = data.get("username")
    password = data.get("password")
    password_confirmation = data.get("password_confirmation")

    if password != password_confirmation:
        return {"errors": ["passwords do not match, try again"]}, 400

    existing_user = User.query.filter_by(username=username).first()

    if existing_user:
        return {"errors": ["Username already exists."]}, 400

    try:
        user = User(username=username)
        user.password = password

        db.session.add(user)
        db.session.commit()
    except ValueError as e:
        return {"errors": [str(e)]}, 400

    token = create_access_token(identity=str(user.id))

    return{
        "token" : token,
        "user" : user_schema.dump(user)
    }, 201

@app.post("/login")
def login():
    data = request.get_json()

    username = data.get("username")
    password = data.get("password")

    user = User.query.filter_by(username=username).first()

    if not user or not user.authenticate(password):
        return {"errors": ["Invalid username or password."]}, 401

    token = create_access_token(identity=str(user.id))

    return {
        "token": token,
        "user": user_schema.dump(user)
    }, 200 

@app.get("/me")
@jwt_required()
def me():
    user_id = int(get_jwt_identity())
    user = User.query.get(user_id)

    if not user:
        return{"errors": ["User not found."]}, 404

    return user_schema.dump(user), 200




@app.post("/tasks")
@jwt_required()
def create_task():
    user_id = int(get_jwt_identity())
    data = request.get_json()

    title = data.get("title")
    description = data.get("description")
    completed = data.get("completed", False)

    try:
        task = Task(
            title=title,
            description=description,
            completed=completed,
            user_id=user_id
        )
        db.session.add(task)
        db.session.commit()

    except ValueError as e:
        return{"errors": [str(e)]}, 400

    return task_schema.dump(task), 201

@app.get("/tasks")
@jwt_required()
def get_tasks():
    user_id = int(get_jwt_identity())

    page = request.args.get("page", 1, type=int)
    per_page = request.args.get("per_page", 5, type=int)

    pagination = Task.query.filter_by(user_id=user_id).paginate(
        page=page,
        per_page=per_page,
        error_out=False
    )

    return {
        "tasks":tasks_schema.dump(pagination.items),
        "page" : pagination.page,
        "pages" : pagination.pages,
        "total" : pagination.total

    }, 200

@app.patch("/tasks/<int:id>")
@jwt_required()
def update_task(id):
    user_id = int(get_jwt_identity())

    task = Task.query.get(id)

    if not task:
        return {"errors": ["Task not found."]}, 404

    if task.user_id != user_id:
        return {"errors": ["Forbidden."]}, 403

    data = request.get_json()

    try:
        if "title" in data:
            task.title = data["title"]
        if "description" in data:
            task.description = data["description"]
        if "completed" in data:
            task.completed = data["completed"]

        db.session.commit()
    except ValueError as e:
        return {"errors": [str(e)]}, 400

    return task_schema.dump(task), 200

@app.delete("/tasks/<int:id>")
@jwt_required()
def delete_task(id):
    user_id = int(get_jwt_identity())
    task = Task.query.get(id)

    if not task:
        return {"errors": ["Task not found."]}, 404
    if task.user_id != user_id:
        return {"errors": ["Forbidden."]}, 403

    db.session.delete(task)
    db.session.commit()

    return {"message": "Task deleted successfully!"}, 200
    


if __name__ == "__main__":
    app.run(port=5555, debug=True)