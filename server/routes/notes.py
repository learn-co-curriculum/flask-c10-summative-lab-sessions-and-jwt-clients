from flask import Blueprint, request, session
from server.models import db, Note
from server.schemas import note_schema, notes_schema
from server.decorators import login_required

notes_bp = Blueprint("notes", __name__)


@notes_bp.route("/notes", methods=["GET"])
@login_required
def get_notes():
    user_id = session.get("user_id")

    page = request.args.get("page", 1, type=int)
    per_page = request.args.get("per_page", 10, type=int)

    pagination = Note.query.filter_by(user_id=user_id).paginate(
        page=page,
        per_page=per_page,
        error_out=False,
    )

    return {
        "notes": notes_schema.dump(pagination.items),
        "total": pagination.total,
        "pages": pagination.pages,
        "current_page": page,
        "per_page": per_page,
    }, 200


@notes_bp.route("/notes/<int:id>", methods=["GET"])
@login_required
def get_note(id):
    user_id = session.get("user_id")

    note = Note.query.filter_by(
        id=id,
        user_id=user_id,
    ).first()

    if not note:
        return {"error": "Note not found"}, 404

    return note_schema.dump(note), 200


@notes_bp.route("/notes", methods=["POST"])
@login_required
def create_note():
    user_id = session.get("user_id")

    data = request.get_json()

    if not data.get("title") or not data.get("content"):
        return {"error": "Title and content are required"}, 422

    note = Note(
        title=data["title"],
        content=data["content"],
        category=data.get("category", "General"),
        user_id=user_id,
    )

    db.session.add(note)
    db.session.commit()

    return note_schema.dump(note), 201


@notes_bp.route("/notes/<int:id>", methods=["PATCH"])
@login_required
def update_note(id):
    user_id = session.get("user_id")

    note = Note.query.filter_by(
        id=id,
        user_id=user_id,
    ).first()

    if not note:
        return {"error": "Note not found"}, 404

    data = request.get_json()

    if "title" in data:
        note.title = data["title"]

    if "content" in data:
        note.content = data["content"]

    if "category" in data:
        note.category = data["category"]

    db.session.commit()

    return note_schema.dump(note), 200


@notes_bp.route("/notes/<int:id>", methods=["DELETE"])
@login_required
def delete_note(id):
    user_id = session.get("user_id")

    note = Note.query.filter_by(
        id=id,
        user_id=user_id,
    ).first()

    if not note:
        return {"error": "Note not found"}, 404

    db.session.delete(note)
    db.session.commit()

    return {}, 204