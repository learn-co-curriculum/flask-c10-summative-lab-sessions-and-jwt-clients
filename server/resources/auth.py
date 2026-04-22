from flask import request, session
from flask_restful import Resource
from models import db, User


class Register(Resource):
    def post(self):
        data = request.get_json()

        # Validate required fields
        username = data.get('username')
        email = data.get('email')
        password = data.get('password')

        if not username or not email or not password:
            return {'error': 'Username, email and password are required.'}, 422

        # Check if username already exists
        if User.query.filter_by(username=username).first():
            return {'error': 'Username already taken.'}, 422

        # Check if email already exists
        if User.query.filter_by(email=email).first():
            return {'error': 'Email already registered.'}, 422

        # Create new user
        try:
            user = User(username=username, email=email)
            user.password_hash = password  # triggers bcrypt setter
            db.session.add(user)
            db.session.commit()

            # Log user in immediately after registration
            session['user_id'] = user.id

            return {
                'id': user.id,
                'username': user.username,
                'email': user.email
            }, 201

        except Exception as e:
            db.session.rollback()
            return {'error': str(e)}, 500


class Login(Resource):
    def post(self):
        data = request.get_json()

        username = data.get('username')
        password = data.get('password')

        if not username or not password:
            return {'error': 'Username and password are required.'}, 422

        # Find user by username
        user = User.query.filter_by(username=username).first()

        if not user or not user.authenticate(password):
            return {'error': 'Invalid username or password.'}, 401

        # Set session
        session['user_id'] = user.id

        return {
            'id': user.id,
            'username': user.username,
            'email': user.email
        }, 200


class Logout(Resource):
    def delete(self):
        # Check if user is logged in
        if not session.get('user_id'):
            return {'error': 'No active session.'}, 401

        # Clear session
        session.pop('user_id', None)
        return {}, 204


class CheckSession(Resource):
    def get(self):
        user_id = session.get('user_id')

        if not user_id:
            return {'error': 'Unauthorized. Please log in.'}, 401

        user = User.query.get(user_id)

        if not user:
            return {'error': 'User not found.'}, 404

        return {
            'id': user.id,
            'username': user.username,
            'email': user.email
        }, 200