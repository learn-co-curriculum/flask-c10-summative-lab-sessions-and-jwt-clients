import pytest
from server.app import app as flask_app
from server.models import db


@pytest.fixture
def app():
    """Flask app with a clean database for each test."""
    flask_app.config["TESTING"] = True
    flask_app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
    flask_app.config["WTF_CSRF_ENABLED"] = False

    with flask_app.app_context():
        db.create_all()
        yield flask_app
        db.session.remove()
        db.drop_all()


@pytest.fixture
def client(app):
    """Anonymous (not logged in) test client."""
    return app.test_client()


@pytest.fixture
def auth_client(client):
    """Test client that is already signed up and logged in."""
    signup = client.post("/signup", json={"username": "tester", "password": "pass1234"})
    login = client.post("/login", json={"username": "tester", "password": "pass1234"})
    assert signup.status_code in (200, 201), signup.get_json()
    assert login.status_code == 200, login.get_json()
    return client