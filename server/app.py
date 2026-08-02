import os
from flask import Flask, request, session
from flask_restful import Api, Resource
from flask_migrate import Migrate

from models import db, bcrypt, User, Note
from schemas import user_schema, note_schema, notes_schema

app =Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = os.environ.get('SECRET_KEY', 'vincent-maina-final-project5')

db.init_app(app)
bcrypt.init_app(app)
migrate = Migrate(app, db)
api = Api(app)

#fucntion to fetch currently logged in user
def get_current_user():
    user_id = session.get('user_id')
    if user_id:
        return User.query.get(user_id)
    return None

#auth endpoints
class Signup(Resource):
    def post(self):
        data = request.get_json()
        errors = user_schema.validate(data)
        if errors:
            return errors, 400
        if User.query.filter_by(username=data['username']).first():
            return {'error': 'Username already exists'}, 400
        #create a new user instance
        user = User(username=data['username'])
        #set the password using the setter method
        user.password_hash = data['password']
        #add the user to the database
        db.session.add(user)
        #commit the user to the database
        db.session.commit()
        session['user_id'] = user.id
        return user_schema.dump(user), 201

class Login(Resource):
    def post(self):
        data = request.get_json()
        errors = user_schema.validate(data)
        if errors:
            return errors, 400
        user = User.query.filter_by(username=data['username']).first()
        #authenticate the user using the authenticate method in the User model
        if user and user.authenticate(data['password']):
            session['user_id'] = user.id
            return user_schema.dump(user), 200
        return {'error': 'Invalid credentials'}, 401

class Logout(Resource):
    def delete(self):
        if session.get('user_id'):
            session.pop('user_id', None)
            return {}, 204
        return {'error': 'Unauthorized'}, 401

#note endpoints with auth
class Checksession(Resource):
    def get(self):
        user = get_current_user()
        if user:
            return user_schema.dump(user), 200
        return {'error': 'Unauthorized'}, 401

#NOTES endpoints
class NotesList(Resource):
    def get(self):
        user = get_current_user()
        if not user:
            return {'error': 'Unauthorized'}, 401
        
        #pagination logic that is required
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 5, type=int)

        notes_pagination = Note.query.filter_by(user_id=user.id).paginate(
            page=page, per_page=per_page, error_out=False
        )
        return {
            'notes': notes_schema.dump(notes_pagination.items),
            'total': notes_pagination.total,
            'page': notes_pagination.page,
            'pages': notes_pagination.pages
        }, 200

    def post(self):
        user = get_current_user()
        if not user:
            return {'error': 'Unauthorized'}, 401

        data = request.get_json()
        errors = note_schema.validate(data)
        if errors:
            return errors, 400
        
        #create a new note instance
        note = Note(
            title = data['title'],
            content = data['content'],
            user_id = user.id
        )

        db.session.add(note)
        db.session.commit()

        return note_schema.dump(note), 201

class NoteResource(Resource):
    #update note
    def patch(self, id):
        user = get_current_user()
        if not user:
            return {'error': 'Unauthorized'}, 401
        note = Note.query.get(id)
        if not note:
            return {'error': 'Note not found'}, 404
        if note.user_id != user.id:
            return {'error': 'Forbidden: You do not own this note'}, 403

        json_data = request.get_json()
        if 'title' in json_data:
            note.title = json_data['title']
        if 'content' in json_data:
            note.content = json_data['content']

        db.session.commit()
        return note_schema.dump(note), 200

    def delete(self, id):#delete note
        user = get_current_user()
        if not user:
            return {'error': 'Unauthorized'}, 401
        note = Note.query.get(id)
        if not note:
            return {'error': 'Note not found'}, 404
        if note.user_id != user.id:
            return {'error': 'Forbidden: You do not own this note'}, 403
        db.session.delete(note)
        db.session.commit()
        return {'message': 'Note deleted successfully'}, 200



#registering my API routes
api.add_resource(Signup, '/signup')
api.add_resource(Login, '/login')
api.add_resource(Logout, '/logout')
api.add_resource(Checksession, '/check_session')

api.add_resource(NotesList, '/notes')
api.add_resource(NoteResource, '/notes/<int:id>')


if __name__ == '__main__':
    app.run(port=5555, debug=True)