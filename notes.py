from flask import Blueprint, request
from extensions import db
from models import Note
from flask_jwt_extended import jwt_required, get_jwt_identity

notes_bp = Blueprint('notes_bp', __name__)

@notes_bp.route('/notes', methods=['POST'])
@jwt_required()
def get_note():
    user_id = get_jwt_identity()
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)

    pagination = Note.query.filter_by(user_id=user_id).paginate(page=page, per_page=per_page, error_out=False)

    return {
        "notes": [note.to_dict() for note in pagination.items],
        "total": pagination.total,
        "pages": pagination.pages,
        "current_page": pagination.page,
        "per_page": per_page
    }, 200

@notes_bp.route('/notes', methods=['POST'])
@jwt_required()
def create_note():
    user_id = get_jwt_identity()
    data = request.get_json()

    if not data.get('title') or not data.get('content'):
        return {"error": "Title and content are required"}, 400

    note = Note(title=data['title'], content=data['content'], user_id=user_id)
    db.session.add(note)
    db.session.commit()
    return note.to_dict(), 201

@notes_bp.route('/notes/<int:note_id>', methods=['PUT'])
@jwt_required()
def update_note(note_id):
    user_id = get_jwt_identity()
    note = Note.query.get_or_404(note_id)

    if note.user_id != user_id:
        return {"error": "Forbidden"}, 403

    data = request.get_json()
    if data.get('title'):
        note.title = data['title']
    if data.get('content'):
        note.content = data['content']

    db.session.commit()
    return note.to_dict(), 200

@notes_bp.route('/notes/<int:note_id>', methods=['DELETE'])
@jwt_required()
def delete_note(note_id):
    user_id = get_jwt_identity()
    note = Note.query.get_or_404(note_id)

    if note.user_id != user_id:
        return {"error": "Forbidden"}, 403

    db.session.delete(note)
    db.session.commit()
    return {}, 204