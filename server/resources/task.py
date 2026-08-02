from flask import request
from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity

from config import db
from models import Task


class TaskList(Resource):

    @jwt_required()
    def get(self):
        user_id = get_jwt_identity()

        page = request.args.get("page", 1, type=int)
        per_page = request.args.get("per_page", 5, type=int)

        tasks = (
            Task.query
            .filter_by(user_id=user_id)
            .paginate(page=page, per_page=per_page, error_out=False)
        )

        return {
            "tasks": [task.to_dict() for task in tasks.items],
            "page": tasks.page,
            "pages": tasks.pages,
            "total": tasks.total
        }, 200

    @jwt_required()
    def post(self):
        user_id = get_jwt_identity()

        data = request.get_json()

        task = Task(
            title=data.get("title"),
            description=data.get("description"),
            status=data.get("status", "Pending"),
            user_id=user_id
        )

        db.session.add(task)
        db.session.commit()

        return task.to_dict(), 201


class TaskResource(Resource):

    @jwt_required()
    def get(self, id):
        user_id = get_jwt_identity()

        task = Task.query.filter_by(id=id, user_id=user_id).first()

        if not task:
            return {"error": "Task not found"}, 404

        return task.to_dict(), 200

    @jwt_required()
    def patch(self, id):
        user_id = get_jwt_identity()

        task = Task.query.filter_by(id=id, user_id=user_id).first()

        if not task:
            return {"error": "Task not found"}, 404

        data = request.get_json()

        if "title" in data:
            task.title = data["title"]

        if "description" in data:
            task.description = data["description"]

        if "status" in data:
            task.status = data["status"]

        db.session.commit()

        return task.to_dict(), 200

    @jwt_required()
    def delete(self, id):
        user_id = get_jwt_identity()

        task = Task.query.filter_by(id=id, user_id=user_id).first()

        if not task:
            return {"error": "Task not found"}, 404

        db.session.delete(task)
        db.session.commit()

        return {"message": "Task deleted successfully"}, 200