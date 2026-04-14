from flask import request
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_restful import Resource
from models import Note, db

class NotesResource(Resource):
    @jwt_required()
    def get(self):
        user_id = get_jwt_identity()
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        notes = Note.query.filter_by(user_id=user_id).paginate(page=page, per_page=per_page)
        note_list = []
        for n in notes.items:
            note_list.append({"id": n.id, "title": n.title, "content": n.content})
        return {
            "notes": note_list,
            "total": notes.total,
            "pages": notes.pages,
            "page": page
        }, 200

    @jwt_required()
    def post(self):
        user_id = get_jwt_identity()
        data = request.get_json()
        if not data or not data.get('title') or not data.get('content'):
            return {"error": "Title and content are required"}, 400
        title = str(data['title'])
        content = str(data['content'])
        note = Note(title=title, content=content, user_id=user_id)
        db.session.add(note)
        db.session.commit()
        return {"id": note.id, "title": note.title, "content": note.content}, 201

class NoteResource(Resource):
    @jwt_required()
    def get(self, note_id):
        user_id = get_jwt_identity()
        note = Note.query.filter_by(id=note_id, user_id=user_id).first()
        if note is None:
            return {"error": "Note not found or not yours"}, 404
        return {"id": note.id, "title": note.title, "content": note.content}, 200

    @jwt_required()
    def patch(self, note_id):
        user_id = get_jwt_identity()
        note = Note.query.filter_by(id=note_id, user_id=user_id).first()
        if note is None:
            return {"error": "Note not found"}, 404
        data = request.get_json()
        if data is None:
            return {"error": "No data provided"}, 400
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
        if note is None:
            return {"error": "Note not found"}, 404
        db.session.delete(note)
        db.session.commit()
        return {"message": "Note deleted successfully"}, 200