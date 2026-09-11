from functools import wraps

from flask import Blueprint, g, jsonify, request
from flask_jwt_extended import get_jwt_identity, jwt_required
from marshmallow import ValidationError

from server import db
from server.models.task import Task
from server.schemas import task_data, task_schema, tasks_schema


tasks_bp = Blueprint("tasks", __name__, url_prefix="/tasks")


def authenticated_route(view):
	@wraps(view)
	@jwt_required()
	def wrapped(*args, **kwargs):
		g.current_user_id = int(get_jwt_identity())
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
		"tasks": tasks_schema.dump(pagination.items),
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
	try:
		task = task_schema.load(payload, session=db.session)
	except ValidationError as exc:
		return jsonify({"errors": [exc.messages]}), 422
	task.user_id = g.current_user_id
	db.session.add(task)
	db.session.commit()
	return jsonify(task_schema.dump(task)), 201


@tasks_bp.get("/<int:task_id>")
@authenticated_route
def get_task(task_id):
	task = task_or_404(task_id)
	if not task:
		return jsonify({"errors": ["Task not found."]}), 404
	return jsonify(task_schema.dump(task))


@tasks_bp.patch("/<int:task_id>")
@authenticated_route
def update_task(task_id):
	task = task_or_404(task_id)
	if not task:
		return jsonify({"errors": ["Task not found."]}), 404
	payload, error = task_data(request.get_json(silent=True), partial=True)
	if error:
		return jsonify({"errors": [error]}), 422
	try:
		task_schema.load(payload, instance=task, partial=True, session=db.session)
	except ValidationError as exc:
		return jsonify({"errors": [exc.messages]}), 422
	db.session.commit()
	return jsonify(task_schema.dump(task))


@tasks_bp.delete("/<int:task_id>")
@authenticated_route
def delete_task(task_id):
	task = task_or_404(task_id)
	if not task:
		return jsonify({"errors": ["Task not found."]}), 404
	db.session.delete(task)
	db.session.commit()
	return jsonify({}), 204
