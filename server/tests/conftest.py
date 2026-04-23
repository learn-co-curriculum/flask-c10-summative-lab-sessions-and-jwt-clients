"""
Shared pytest fixtures.

All tests use an in-memory SQLite database so they are fast, isolated, and
leave no artefacts on disk.
"""

import pytest

from app import create_app
from app.extensions import db as _db
from app.models.user import User
from app.models.note import Note, Tag
from app.config import TestingConfig


@pytest.fixture(scope="function")
def app():
    """Create a fresh application instance for each test function."""
    application = create_app(TestingConfig)
    with application.app_context():
        _db.create_all()
        yield application
        _db.session.remove()
        _db.drop_all()


@pytest.fixture
def client(app):
    """Flask test client."""
    return app.test_client()


@pytest.fixture
def db(app):
    """Database session bound to the test app context."""
    return _db


@pytest.fixture
def alice(db):
    """A persisted test user."""
    user = User(username="alice@example.com")
    user.set_password("password123")
    db.session.add(user)
    db.session.commit()
    return user


@pytest.fixture
def bob(db):
    """A second persisted test user."""
    user = User(username="bob@example.com")
    user.set_password("password123")
    db.session.add(user)
    db.session.commit()
    return user


@pytest.fixture
def alice_token(client, alice):
    """JWT token for alice obtained via the login endpoint."""
    resp = client.post(
        "/login", json={"username": "alice@example.com", "password": "password123"}
    )
    return resp.get_json()["token"]


@pytest.fixture
def alice_note(db, alice):
    """A note owned by alice."""
    note = Note(user_id=alice.id, title="Alice's Note", content="Some content.")
    db.session.add(note)
    db.session.commit()
    return note


@pytest.fixture
def alice_tag(db, alice):
    """A tag owned by alice."""
    tag = Tag(user_id=alice.id, name="Work", color="#3B82F6")
    db.session.add(tag)
    db.session.commit()
    return tag
