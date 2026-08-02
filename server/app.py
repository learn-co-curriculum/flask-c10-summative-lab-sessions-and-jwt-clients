#!/usr/bin/env python3

from flask import Flask, request, session
from flask_migrate import Migrate
from sqlalchemy.exc import IntegrityError

from models import db, bcrypt, User, Note

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = b'change-this-later-for-real-use'

migrate = Migrate(app, db)

db.init_app(app)
bcrypt.init_app(app)

@app.route('/signup', methods=['POST'])
def signup():
    data = request.get_json()

    username = data.get('username')
    password = data.get('password')
    password_confirmation = data.get('password_confirmation')

    if password != password_confirmation:
        return {'errors': ['Passwords do not match']}, 422

    try:
        user = User(username=username)
        user.password_hash = password

        db.session.add(user)
        db.session.commit()

        session['user_id'] = user.id

        return {'id': user.id, 'username': user.username}, 201

    except IntegrityError:
        db.session.rollback()
        return {'errors': ['Username already taken']}, 422

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()

    username = data.get('username')
    password = data.get('password')

    user = User.query.filter(User.username == username).first()

    if user and user.authenticate(password):
        session['user_id'] = user.id
        return {'id': user.id, 'username': user.username}, 200

    return {'errors': ['Invalid username or password']}, 401

@app.route('/check_session')
def check_session():
    user_id = session.get('user_id')

    if user_id:
        user = User.query.filter(User.id == user_id).first()
        if user:
            return {'id': user.id, 'username': user.username}, 200

    return {}, 401

@app.route('/logout', methods=['DELETE'])
def logout():
    session['user_id'] = None
    return {}, 204

if __name__ == '__main__':
    app.run(port=5555, debug=True)