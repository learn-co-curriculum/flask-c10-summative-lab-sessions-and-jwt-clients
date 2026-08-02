import pytest

from server.app import create_app
from server.models import db


@pytest.fixture()
def app():
    test_app = create_app(
        {
            "TESTING": True,
            "SECRET_KEY": (
                "testing-secret-key"
            ),
            "SQLALCHEMY_DATABASE_URI": (
                "sqlite:///:memory:"
            ),
        }
    )

    with test_app.app_context():
        db.create_all()

        yield test_app

        db.session.remove()
        db.drop_all()


@pytest.fixture()
def client(app):
    return app.test_client()