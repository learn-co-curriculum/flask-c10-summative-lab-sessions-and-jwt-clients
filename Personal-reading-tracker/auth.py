from functools import wraps

from flask import Blueprint, current_app, g, jsonify, request, session
from flask_bcrypt import Bcrypt
from marshmallow import ValidationError
from sqlalchemy import or_
from sqlalchemy.exc import IntegrityError

from auth_schemas import LoginSchema, PublicUserSchema, RegistrationSchema
from models import User, db

auth = Blueprint('auth', __name__)
bcrypt = Bcrypt()
user_schema = PublicUserSchema()


def error(message, status):
    return jsonify(errors=[message]), status


def login_required(view):
    @wraps(view)
    def wrapped(*args, **kwargs):
        user_id = session.get('user_id')
        g.current_user = db.session.get(User, user_id) if isinstance(user_id, int) else None
        if g.current_user is None:
            session.clear()
            return error('Authentication required.', 401)
        return view(*args, **kwargs)
    return wrapped


def protect_routes():
    # Reject cross-origin writes and form submissions for cookie authentication.
    if request.method in {'POST', 'PUT', 'PATCH', 'DELETE'}:
        origin = request.headers.get('Origin')
        if origin and origin not in current_app.config['TRUSTED_ORIGINS']:
            return error('Request origin is not allowed.', 403)
        if request.method != 'DELETE' and not request.is_json:
            return error('Send a JSON request body.', 400)
    public = {'auth.register', 'auth.login', 'static'}
    if request.endpoint and request.endpoint not in public and request.method != 'OPTIONS':
        return login_required(lambda: None)()


def load_request(schema):
    data = request.get_json(silent=True)
    if not isinstance(data, dict):
        raise ValidationError({'body': ['Expected a JSON object.']})
    return schema.load(data)


@auth.errorhandler(ValidationError)
def invalid_input(exc):
    messages = [f'{field}: {message}' for field, items in exc.messages.items() for message in items]
    return jsonify(errors=messages), 400


def start_session(user):
    session.clear()
    session['user_id'] = user.id
    session.permanent = True


@auth.post('/register')
@auth.post('/signup')
def register():
    data = load_request(RegistrationSchema())
    email = data['email'].lower()
    if User.query.filter(or_(User.username == data['username'], User.email == email)).first():
        return error('Username or email already exists.', 400)
    user = User(username=data['username'], email=email,
                password_hash=bcrypt.generate_password_hash(data['password']).decode('utf-8'))
    db.session.add(user)
    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        return error('Username or email already exists.', 400)
    start_session(user)
    return jsonify(user_schema.dump(user)), 201


@auth.post('/login')
def login():
    data = load_request(LoginSchema())
    user = User.query.filter_by(username=data['username']).first()
    if user is None or not bcrypt.check_password_hash(user.password_hash, data['password']):
        return error('Invalid username or password.', 401)
    start_session(user)
    return jsonify(user_schema.dump(user)), 200


@auth.get('/check_session')
@login_required
def check_session():
    return jsonify(user_schema.dump(g.current_user)), 200


@auth.delete('/logout')
@login_required
def logout():
    session.clear()
    return '', 204
