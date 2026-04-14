from flask import request
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_restful import Resource
from models import Note, db

class NotesResource(Resource):
    """Handle notes list and creation"""
    @jwt_required()
    def get(self):
        # Get user id from token
        user_id = get_jwt_identity()
        # Get pagination params
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        # Query notes for user
        notes = Note.query.filter_by(user_id=user_id).paginate(page=page, per_page=per_page)
        return {
            "notes": [{"id": n.id, "title": n.title, "content": n.content} for n in notes.items],
            "total": notes.total,
            "pages": notes.pages,
            "page": page
        }, 200

    @jwt_required()
    def post(self):
        # Get user id
        user_id = get_jwt_identity()
        data = request.get_json()
        # Validate data
        if not data.get('title') or not data.get('content'):
            return {"error": "Title and content required"}, 400
        # Create note
        note = Note(title=data['title'], content=data['content'], user_id=user_id)
        db.session.add(note)
        db.session.commit()
        return {"id": note.id, "title": note.title, "content": note.content}, 201

class NoteResource(Resource):
    """Handle single note operations"""
    @jwt_required()
    def get(self, note_id):
        user_id = get_jwt_identity()
        # Find note by id and user
        note = Note.query.filter_by(id=note_id, user_id=user_id).first()
        if not note:
            return {"error": "Note not found"}, 404
        return {"id": note.id, "title": note.title, "content": note.content}, 200

    @jwt_required()
    def patch(self, note_id):
        user_id = get_jwt_identity()
        note = Note.query.filter_by(id=note_id, user_id=user_id).first()
        if not note:
            return {"error": "Note not found"}, 404
        data = request.get_json()
        # Update fields
        if 'title' in data:
            note.title = data['title']
        if 'content' in data:
            note.content = data['content']
        db.session.commit()
        return {"id": note.id, "title": note.title, "content": note.content}, 200

    @jwt_required()
    def delete(self, note_id):
        user_id = get_jwt_identity()
        note = Note.query.filter_by(id=note_id, user_id=user_id).first()
        if not note:
            return {"error": "Note not found"}, 404
        # Delete note
        db.session.delete(note)
        db.session.commit()
        return {"message": "Note deleted"}, 200