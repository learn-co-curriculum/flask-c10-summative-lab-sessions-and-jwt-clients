"""Protected CRUD routes for the Note resource.

Every route requires login, and every query is tied to the current user, so one
user can never read or change another user's notes.
"""
from flask import g, request
from flask_restful import Resource
from marshmallow import ValidationError

from config import db
from models import Note
from schemas import note_schema, notes_schema
from utils import format_errors, login_required

DEFAULT_PER_PAGE = 10
MAX_PER_PAGE = 100


def get_owned_note(note_id):
    """Return (note, None) if the current user owns it, else (None, error_response)."""
    note = db.session.get(Note, note_id)
    if note is None:
        return None, ({"errors": ["Note not found."]}, 404)
    if note.user_id != g.current_user.id:
        return None, ({"errors": ["Forbidden: this note belongs to another user."]}, 403)
    return note, None


class NoteList(Resource):
    method_decorators = [login_required]

    def get(self):
        """GET /notes?page=1&per_page=10 - paginated notes for the current user."""
        page = request.args.get("page", default=1, type=int)
        per_page = request.args.get("per_page", default=DEFAULT_PER_PAGE, type=int)
        if page < 1 or per_page < 1:
            return {"errors": ["page and per_page must be positive integers."]}, 400
        per_page = min(per_page, MAX_PER_PAGE)

        pagination = (
            Note.query.filter_by(user_id=g.current_user.id)
            .order_by(Note.is_pinned.desc(), Note.created_at.desc(), Note.id.desc())
            .paginate(page=page, per_page=per_page, error_out=False)
        )
        return {
            "notes": notes_schema.dump(pagination.items),
            "page": pagination.page,
            "per_page": pagination.per_page,
            "total": pagination.total,
            "pages": pagination.pages,
            "has_next": pagination.has_next,
            "has_prev": pagination.has_prev,
        }, 200

    def post(self):
        """POST /notes - create a note owned by the current user."""
        try:
            data = note_schema.load(request.get_json(silent=True) or {})
        except ValidationError as err:
            return {"errors": format_errors(err.messages)}, 422

        note = Note(**data, user_id=g.current_user.id)
        db.session.add(note)
        db.session.commit()
        return note_schema.dump(note), 201


class NoteDetail(Resource):
    method_decorators = [login_required]

    def get(self, note_id):
        """GET /notes/<id> - fetch one of the current user's notes."""
        note, error = get_owned_note(note_id)
        if error:
            return error
        return note_schema.dump(note), 200

    def patch(self, note_id):
        """PATCH /notes/<id> - partially update one of the current user's notes."""
        note, error = get_owned_note(note_id)
        if error:
            return error

        payload = request.get_json(silent=True)
        if not isinstance(payload, dict) or not payload:
            return {"errors": ["Request body must be a non-empty JSON object."]}, 400

        try:
            data = note_schema.load(payload, partial=True)
        except ValidationError as err:
            return {"errors": format_errors(err.messages)}, 422

        for key, value in data.items():
            setattr(note, key, value)
        db.session.commit()
        return note_schema.dump(note), 200

    def delete(self, note_id):
        """DELETE /notes/<id> - delete one of the current user's notes."""
        note, error = get_owned_note(note_id)
        if error:
            return error
        db.session.delete(note)
        db.session.commit()
        return "", 204