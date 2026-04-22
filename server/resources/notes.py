from flask import request, session
from flask_restful import Resource
from models import db, Note


def get_current_user_id():
    """Helper to get current user_id from session."""
    return session.get('user_id')


class NoteList(Resource):
    def get(self):
        user_id = get_current_user_id()
        if not user_id:
            return {'error': 'Unauthorized. Please log in.'}, 401

        # Pagination parameters
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 5, type=int)

        # Query only the logged-in user's notes
        pagination = Note.query.filter_by(user_id=user_id)\
            .order_by(Note.created_at.desc())\
            .paginate(page=page, per_page=per_page, error_out=False)

        return {
            'notes': [note.to_dict() for note in pagination.items],
            'total': pagination.total,
            'pages': pagination.pages,
            'current_page': pagination.page,
            'per_page': per_page
        }, 200

    def post(self):
        user_id = get_current_user_id()
        if not user_id:
            return {'error': 'Unauthorized. Please log in.'}, 401

        data = request.get_json()
        title = data.get('title')
        content = data.get('content')

        if not title or not content:
            return {'error': 'Title and content are required.'}, 422

        try:
            note = Note(title=title, content=content, user_id=user_id)
            db.session.add(note)
            db.session.commit()
            return note.to_dict(), 201

        except Exception as e:
            db.session.rollback()
            return {'error': str(e)}, 500


class NoteDetail(Resource):
    def get(self, id):
        user_id = get_current_user_id()
        if not user_id:
            return {'error': 'Unauthorized. Please log in.'}, 401

        note = Note.query.get(id)

        if not note:
            return {'error': 'Note not found.'}, 404

        # Ensure user owns this note
        if note.user_id != user_id:
            return {'error': 'Forbidden. You do not own this note.'}, 403

        return note.to_dict(), 200

    def patch(self, id):
        user_id = get_current_user_id()
        if not user_id:
            return {'error': 'Unauthorized. Please log in.'}, 401

        note = Note.query.get(id)

        if not note:
            return {'error': 'Note not found.'}, 404

        # Ensure user owns this note
        if note.user_id != user_id:
            return {'error': 'Forbidden. You do not own this note.'}, 403

        data = request.get_json()

        # Only update fields that are provided
        if 'title' in data:
            note.title = data['title']
        if 'content' in data:
            note.content = data['content']

        try:
            db.session.commit()
            return note.to_dict(), 200

        except Exception as e:
            db.session.rollback()
            return {'error': str(e)}, 500

    def delete(self, id):
        user_id = get_current_user_id()
        if not user_id:
            return {'error': 'Unauthorized. Please log in.'}, 401

        note = Note.query.get(id)

        if not note:
            return {'error': 'Note not found.'}, 404

        # Ensure user owns this note
        if note.user_id != user_id:
            return {'error': 'Forbidden. You do not own this note.'}, 403

        try:
            db.session.delete(note)
            db.session.commit()
            return {}, 204

        except Exception as e:
            db.session.rollback()
            return {'error': str(e)}, 500