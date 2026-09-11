from functools import wraps

from flask import Blueprint, g, jsonify, request, session
from flask_jwt_extended import get_jwt_identity, verify_jwt_in_request

from server import db
from server.models.task import Task
from server.models.user import User
from server.schemas import task_data


tasks_bp = Blueprint("tasks", __name__, url_prefix="/tasks")


def authenticated_route(view):
	@wraps(view)
	def wrapped(*args, **kwargs):
		has_bearer_token = request.headers.get("Authorization", "").startswith("Bearer ")
		if has_bearer_token:
			try:
				verify_jwt_in_request()
				identity = get_jwt_identity()
			except Exception:
				return jsonify({"errors": ["Invalid or expired token."]}), 401
		else:
			identity = None
		user_id = int(identity) if identity is not None else session.get("user_id")
		if not user_id or not db.session.get(User, user_id):
			return jsonify({"errors": ["Authentication required."]}), 401
		g.current_user_id = user_id
		return view(*args, **kwargs)
	return wrapped


def task_or_404(task_id):
	task = db.session.get(Task, task_id)
	if not task or task.user_id != g.current_user_id:
		return None
	return task


@tasks_bp.get("")
@authenticated_route
def list_tasks():
	page = max(request.args.get("page", 1, type=int), 1)
	per_page = min(max(request.args.get("per_page", 10, type=int), 1), 100)
	pagination = Task.query.filter_by(user_id=g.current_user_id).order_by(Task.id).paginate(
		page=page, per_page=per_page, error_out=False
	)
	return jsonify({
		"tasks": [task.to_dict() for task in pagination.items],
		"page": pagination.page,
		"per_page": pagination.per_page,
		"pages": pagination.pages,
		"total": pagination.total,
		"has_next": pagination.has_next,
		"has_prev": pagination.has_prev,
	})


@tasks_bp.post("")
@authenticated_route
def create_task():
	payload, error = task_data(request.get_json(silent=True))
	if error:
		return jsonify({"errors": [error]}), 422
	task = Task(
		title=payload["title"],
		description=payload.get("description"),
		completed=payload.get("completed", False),
		user_id=g.current_user_id,
	)
	db.session.add(task)
	db.session.commit()
	return jsonify(task.to_dict()), 201


@tasks_bp.get("/<int:task_id>")
@authenticated_route
def get_task(task_id):
	task = task_or_404(task_id)
	if not task:
		return jsonify({"errors": ["Task not found."]}), 404
	return jsonify(task.to_dict())


@tasks_bp.patch("/<int:task_id>")
@authenticated_route
def update_task(task_id):
	task = task_or_404(task_id)
	if not task:
		return jsonify({"errors": ["Task not found."]}), 404
	payload, error = task_data(request.get_json(silent=True), partial=True)
	if error:
		return jsonify({"errors": [error]}), 422
	for field, value in payload.items():
		setattr(task, field, value)
	db.session.commit()
	return jsonify(task.to_dict())


@tasks_bp.delete("/<int:task_id>")
@authenticated_route
def delete_task(task_id):
	task = task_or_404(task_id)
	if not task:
		return jsonify({"errors": ["Task not found."]}), 404
	db.session.delete(task)
	db.session.commit()
	return jsonify({}), 204
