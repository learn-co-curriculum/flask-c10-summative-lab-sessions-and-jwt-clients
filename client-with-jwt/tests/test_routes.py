import pytest
from server.app import app
from server.models import db


# FIXTURES & SETUP

pytest.fixture
def client():
    """Configure a clean in-memory database and test client for each test run."""
    app.config["TESTING"] = True
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    with app.app_context():
        db.create_all()
        yield app.test_client()
        db.session.remove()
        db.drop_all()
