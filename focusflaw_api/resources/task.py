from flask import Blueprint, request, jsonify, session

from extensions import db
from models import Task
from schemas import TaskSchema

task_bp = Blueprint("tasks", __name__)

task_schema = TaskSchema()
tasks_schema = TaskSchema(many=True)


@task_bp.route("/tasks", methods=["GET"])
def get_tasks():
    user_id = session.get("user_id")

    if not user_id:
        return jsonify({"Error": "Unauthorized"}), 401

    page = request.args.get("page", 1, type=int)
    per_page = 5

    pagination = Task.query.filter_by(user_id=user_id).paginate(
        page=page,
        per_page=per_page,
        error_out=False
    )

    return jsonify({
        "tasks": tasks_schema.dump(pagination.items),
        "page": pagination.page,
        "pages": pagination.pages,
        "total": pagination.total
    }), 200


@task_bp.route("/tasks", methods=["POST"])
def create_task():
    user_id = session.get("user_id")

    if not user_id:
        return jsonify({"Error": "Unauthorized"}), 401

    data = request.get_json()

    task = Task(
        title=data.get("title"),
        description=data.get("description"),
        completed=False,
        user_id=user_id
    )

    db.session.add(task)
    db.session.commit()

    return task_schema.dump(task), 201


@task_bp.route("/tasks/<int:id>", methods=["PATCH"])
def update_task(id):
    user_id = session.get("user_id")

    if not user_id:
        return jsonify({"Error": "Unauthorized"}), 401

    task = Task.query.filter_by(id=id, user_id=user_id).first()

    if not task:
        return jsonify({"Error": "Task not found"}), 404

    data = request.get_json()

    task.title = data.get("title", task.title)
    task.description = data.get("description", task.description)
    task.completed = data.get("completed", task.completed)

    db.session.commit()

    return task_schema.dump(task), 200


@task_bp.route("/tasks/<int:id>", methods=["DELETE"])
def delete_task(id):
    user_id = session.get("user_id")

    if not user_id:
        return jsonify({"Error": "Unauthorized"}), 401

    task = Task.query.filter_by(id=id, user_id=user_id).first()

    if not task:
        return jsonify({"Error": "Task not found"}), 404

    db.session.delete(task)
    db.session.commit()

    return jsonify({
        "message": "Task deleted successfully"
    }), 200
