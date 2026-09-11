import os

import pytest


os.environ["DATABASE_URL"] = "sqlite:///:memory:"

from server import db  # noqa: E402
from server.app import app  # noqa: E402


@pytest.fixture()
def client():
    app.config.update(TESTING=True)
    with app.app_context():
        db.create_all()
        yield app.test_client()
        db.session.remove()
        db.drop_all()