from flask import Blueprint, request
from models import Note
from config import db
from flask_jwt_extended import jwt_required, get_jwt_identity

notes_bp = Blueprint('notes', __name__)

# =========================
# CREATE NOTE
# =========================
@notes_bp.post('/notes')
@jwt_required()
def create_note():
    user_id = get_jwt_identity()
    data = request.get_json()

    note = Note(
        title=data.get('title'),
        content=data.get('content'),
        category=data.get('category'),
        user_id=int(user_id)
    )

    db.session.add(note)
    db.session.commit()

    return {
        "id": note.id,
        "title": note.title,
        "content": note.content,
        "category": note.category
    }, 201


# =========================
# GET ALL NOTES (WITH PAGINATION)
# =========================
@notes_bp.get('/notes')
@jwt_required()
def get_notes():
    user_id = get_jwt_identity()

    # pagination params
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 5, type=int)

    query = Note.query.filter_by(user_id=int(user_id))

    paginated_notes = query.paginate(page=page, per_page=per_page, error_out=False)

    return {
        "notes": [
            {
                "id": n.id,
                "title": n.title,
                "content": n.content,
                "category": n.category
            }
            for n in paginated_notes.items
        ],
        "total": paginated_notes.total,
        "page": paginated_notes.page,
        "pages": paginated_notes.pages,
        "per_page": paginated_notes.per_page
    }, 200


# =========================
# GET SINGLE NOTE
# =========================
@notes_bp.get('/notes/<int:id>')
@jwt_required()
def get_note(id):
    user_id = get_jwt_identity()

    note = Note.query.filter_by(id=id, user_id=int(user_id)).first()

    if not note:
        return {"error": "Note not found"}, 404

    return {
        "id": note.id,
        "title": note.title,
        "content": note.content,
        "category": note.category
    }, 200


# =========================
# UPDATE NOTE
# =========================
@notes_bp.patch('/notes/<int:id>')
@jwt_required()
def update_note(id):
    user_id = get_jwt_identity()
    data = request.get_json()

    note = Note.query.filter_by(id=id, user_id=int(user_id)).first()

    if not note:
        return {"error": "Note not found"}, 404

    if data.get('title'):
        note.title = data.get('title')

    if data.get('content'):
        note.content = data.get('content')

    if data.get('category') is not None:
        note.category = data.get('category')

    db.session.commit()

    return {
        "id": note.id,
        "title": note.title,
        "content": note.content,
        "category": note.category
    }, 200


# =========================
# DELETE NOTE
# =========================
@notes_bp.delete('/notes/<int:id>')
@jwt_required()
def delete_note(id):
    user_id = get_jwt_identity()

    note = Note.query.filter_by(id=id, user_id=int(user_id)).first()

    if not note:
        return {"error": "Note not found"}, 404

    db.session.delete(note)
    db.session.commit()

    return {"message": "Note deleted"}, 200