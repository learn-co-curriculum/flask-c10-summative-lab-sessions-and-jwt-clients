import os
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
os.environ.setdefault('SECRET_KEY', 'isolated-test-secret-not-for-deployment')
from app import create_app
from auth import bcrypt, login_required
from flask import g
from models import User, db


@pytest.fixture()
def app():
    application = create_app({'TESTING': True, 'SQLALCHEMY_DATABASE_URI': 'sqlite://',
                              'SECRET_KEY': 'test-secret', 'BCRYPT_LOG_ROUNDS': 4})

    @application.route('/private', methods=['GET', 'POST', 'PATCH', 'DELETE'])
    @login_required
    def private():
        return {'user_id': g.current_user.id}

    @application.get('/default-protected')
    def default_protected():
        return {'user_id': g.current_user.id}

    with application.app_context():
        db.create_all()
    yield application
    with application.app_context():
        db.session.remove()
        db.drop_all()


@pytest.fixture()
def client(app):
    return app.test_client()


def register(client, username='ibraanwar', email='ibraanwar@example.com', **extra):
    return client.post('/register', json=dict(username=username, email=email,
                                             password='password123', **extra))


def test_complete_flow(client, app):
    response = register(client)
    assert response.status_code == 201
    assert set(response.json) == {'id', 'username', 'email'}
    assert 'HttpOnly' in response.headers['Set-Cookie']
    assert 'SameSite=Lax' in response.headers['Set-Cookie']
    with app.app_context():
        user = User.query.one()
        assert user.password_hash != 'password123'
        assert bcrypt.check_password_hash(user.password_hash, 'password123')
    assert client.get('/check_session').json == response.json
    assert client.get('/private').status_code == 200
    assert client.get('/default-protected').status_code == 200
    assert client.delete('/logout').status_code == 204
    assert client.get('/check_session').status_code == 401
    assert client.get('/private').status_code == 401
    assert client.post('/login', json={'username': 'ibraanwar', 'password': 'password123'}).status_code == 200


@pytest.mark.parametrize('method', ['get', 'post', 'patch', 'delete'])
def test_unauthenticated_resource_methods(client, method):
    assert getattr(client, method)('/private', json={}).status_code == 401


@pytest.mark.parametrize('payload', [None, [], {}, {'username': 42},
    {'username': 'abc', 'email': 'bad', 'password': 'password123'},
    {'username': 'abc', 'email': 'abc@example.com', 'password': 'short'},
    {'username': 'abc', 'email': 'abc@example.com', 'password': 'a' * 73},
    {'username': 'abc', 'email': 'abc@example.com', 'password': '\u00e9' * 37},
    {'username': 'abc', 'email': 'abc@example.com', 'password': 'password123', 'user_id': 1}])
def test_registration_validation(client, payload):
    response = client.post('/register', json=payload)
    assert response.status_code == 400
    assert 'errors' in response.json


def test_malformed_and_form_requests(client):
    assert client.post('/register', data='{', content_type='application/json').status_code == 400
    assert client.post('/login', data={'username': 'abc', 'password': 'password123'}).status_code == 400


def test_duplicates_and_confirmation(client):
    assert register(client, password_confirmation='different').status_code == 400
    assert register(client).status_code == 201
    assert register(client, email='another@example.com').status_code == 400
    assert register(client, username='other', email='IBRAANWAR@example.com').status_code == 400


def test_bad_login(client):
    register(client)
    client.delete('/logout')
    for username, password in [('ibraanwar', 'wrongpass'), ('missing', 'password123')]:
        response = client.post('/login', json={'username': username, 'password': password})
        assert response.status_code == 401
        assert response.json == {'errors': ['Invalid username or password.']}
    assert client.get('/check_session').status_code == 401


def test_two_users_and_deleted_user(app):
    first, second = app.test_client(), app.test_client()
    first_id = register(first).json['id']
    second_id = register(second, 'other', 'other@example.com').json['id']
    assert first.get('/private').json['user_id'] == first_id
    assert second.get('/private').json['user_id'] == second_id
    first.delete('/logout')
    assert second.get('/check_session').status_code == 200
    with app.app_context():
        db.session.delete(db.session.get(User, second_id))
        db.session.commit()
    assert second.get('/check_session').status_code == 401


def test_origin_protection(client):
    assert client.post('/login', json={}, headers={'Origin': 'https://evil.example'}).status_code == 403
    register(client)
    assert client.delete('/logout', headers={'Origin': 'https://evil.example'}).status_code == 403
    assert client.get('/check_session').status_code == 200
    assert client.delete('/logout', headers={'Origin': 'http://localhost:4000'}).status_code == 204


def test_signup_alias(client):
    response = client.post('/signup', json={'username': 'abc', 'email': 'abc@example.com',
                                           'password': 'password123', 'password_confirmation': 'password123'})
    assert response.status_code == 201


def test_forged_identity(client):
    with client.session_transaction() as session:
        session['user_id'] = 'not-an-integer'
    assert client.get('/check_session').status_code == 401


def test_requires_secret(monkeypatch):
    monkeypatch.delenv('SECRET_KEY', raising=False)
    with pytest.raises(RuntimeError, match='SECRET_KEY'):
        create_app()
