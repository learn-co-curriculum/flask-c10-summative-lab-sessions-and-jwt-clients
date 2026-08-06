import os
from flask import Flask, request, session
from flask_migrate import Migrate
from flask_restful import Api, Resource
from sqlalchemy.exc import IntegrityError
from server.models import User, Task, db, bcrypt
from server.schemas import user_schema, task_schema, tasks_schema

def create_app(test_config=None):
    app = Flask(__name__)
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'development-secret-key')
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URI', 'sqlite:///app.db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    if test_config:
        app.config.update(test_config)
    db.init_app(app)
    bcrypt.init_app(app)
    Migrate(app, db)
    api = Api(app)

    def get_current_user():
        user_id = session.get('user_id')
        if user_id is None:
            return None
        user = db.session.get(User, user_id)
        if user is None:
            session.pop('user_id', None)
        return user

    def get_owned_task(task_id):
        user_id = session.get('user_id')
        if user_id is None:
            return None
        return Task.query.filter_by(id=task_id, user_id=user_id).first()

    class Home(Resource):

        def get(self):
            return ({'message': 'Productivity Task Tracker API', 'status': 'running'}, 200)

    class Signup(Resource):

        def post(self):
            data = request.get_json(silent=True)
            if not isinstance(data, dict):
                return ({'error': 'A JSON request body is required.'}, 400)
            username = data.get('username')
            password = data.get('password')
            password_confirmation = data.get('password_confirmation')
            if not username:
                return ({'error': 'Username is required.'}, 400)
            if not password:
                return ({'error': 'Password is required.'}, 400)
            if not password_confirmation:
                return ({'error': 'Password confirmation is required.'}, 400)
            if password != password_confirmation:
                return ({'error': 'Passwords do not match.'}, 400)
            existing_user = User.query.filter_by(username=username.strip()).first()
            if existing_user:
                return ({'error': 'Username already exists.'}, 409)
            try:
                user = User(username=username)
                user.password = password
                db.session.add(user)
                db.session.commit()
            except ValueError as error:
                db.session.rollback()
                return ({'error': str(error)}, 400)
            except IntegrityError:
                db.session.rollback()
                return ({'error': 'Username already exists.'}, 409)
            session['user_id'] = user.id
            return (user_schema.dump(user), 201)

    class Login(Resource):

        def post(self):
            data = request.get_json(silent=True)
            if not isinstance(data, dict):
                return ({'error': 'A JSON request body is required.'}, 400)
            username = data.get('username')
            password = data.get('password')
            if not username or not password:
                return ({'error': 'Username and password are required.'}, 400)
            user = User.query.filter_by(username=username.strip()).first()
            if user is None or not user.authenticate(password):
                return ({'error': 'Invalid username or password.'}, 401)
            session['user_id'] = user.id
            return (user_schema.dump(user), 200)

    class CheckSession(Resource):

        def get(self):
            user = get_current_user()
            if user is None:
                return ({}, 200)
            return (user_schema.dump(user), 200)

    class Logout(Resource):

        def delete(self):
            session.pop('user_id', None)
            return ({}, 200)

    class Tasks(Resource):

        def get(self):
            user = get_current_user()
            if user is None:
                return ({'error': 'Not authorized.'}, 401)
            page = request.args.get('page', default=1, type=int)
            per_page = request.args.get('per_page', default=5, type=int)
            if page is None or page < 1:
                return ({'error': 'Page must be a positive integer.'}, 400)
            if per_page is None or per_page < 1:
                return ({'error': 'Per-page must be a positive integer.'}, 400)
            per_page = min(per_page, 100)
            pagination = Task.query.filter_by(user_id=user.id).order_by(Task.created_at.desc(), Task.id.desc()).paginate(page=page, per_page=per_page, error_out=False)
            return ({'tasks': tasks_schema.dump(pagination.items), 'pagination': {'page': pagination.page, 'per_page': pagination.per_page, 'total_items': pagination.total, 'total_pages': pagination.pages, 'has_next': pagination.has_next, 'has_prev': pagination.has_prev}}, 200)

        def post(self):
            user = get_current_user()
            if user is None:
                return ({'error': 'Not authorized.'}, 401)
            data = request.get_json(silent=True)
            if not isinstance(data, dict):
                return ({'error': 'A JSON request body is required.'}, 400)
            title = data.get('title')
            if not title:
                return ({'error': 'Title is required.'}, 400)
            try:
                task = Task(title=title, description=data.get('description', ''), completed=data.get('completed', False), user_id=user.id)
                db.session.add(task)
                db.session.commit()
            except ValueError as error:
                db.session.rollback()
                return ({'error': str(error)}, 400)
            return (task_schema.dump(task), 201)

    class TaskById(Resource):

        def get(self, task_id):
            user = get_current_user()
            if user is None:
                return ({'error': 'Not authorized.'}, 401)
            task = get_owned_task(task_id)
            if task is None:
                return ({'error': 'Task not found.'}, 404)
            return (task_schema.dump(task), 200)

        def patch(self, task_id):
            user = get_current_user()
            if user is None:
                return ({'error': 'Not authorized.'}, 401)
            task = get_owned_task(task_id)
            if task is None:
                return ({'error': 'Task not found.'}, 404)
            data = request.get_json(silent=True)
            if not isinstance(data, dict):
                return ({'error': 'A JSON request body is required.'}, 400)
            allowed_fields = {'title', 'description', 'completed'}
            updates = {key: value for key, value in data.items() if key in allowed_fields}
            if not updates:
                return ({'error': 'Provide title, description, or completed.'}, 400)
            try:
                for key, value in updates.items():
                    setattr(task, key, value)
                db.session.commit()
            except ValueError as error:
                db.session.rollback()
                return ({'error': str(error)}, 400)
            return (task_schema.dump(task), 200)

        def delete(self, task_id):
            user = get_current_user()
            if user is None:
                return ({'error': 'Not authorized.'}, 401)
            task = get_owned_task(task_id)
            if task is None:
                return ({'error': 'Task not found.'}, 404)
            db.session.delete(task)
            db.session.commit()
            return ({}, 204)
    api.add_resource(Home, '/')
    api.add_resource(Signup, '/signup')
    api.add_resource(Login, '/login')
    api.add_resource(CheckSession, '/check_session')
    api.add_resource(Logout, '/logout')
    api.add_resource(Tasks, '/tasks')
    api.add_resource(TaskById, '/tasks/<int:task_id>')
    return app
app = create_app()
if __name__ == '__main__':
    app.run(port=5555, debug=True)