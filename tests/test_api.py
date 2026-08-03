import pytest

from app import create_app
from extensions import db


class TestConfig:
    TESTING = True
    SECRET_KEY = "test-secret-key"
    SQLALCHEMY_DATABASE_URI = "sqlite://"
    SQLALCHEMY_TRACK_MODIFICATIONS = False


@pytest.fixture
def client():
    app = create_app(TestConfig)
    with app.app_context():
        db.create_all()
        yield app.test_client()
        db.session.remove()
        db.drop_all()


def signup(client, username="testuser"):
    return client.post(
        "/signup",
        json={
            "username": username,
            "password": "password123",
            "password_confirmation": "password123",
        },
    )


def create_note(client, title="First note", content="A private note"):
    return client.post("/notes", json={"title": title, "content": content})


def test_signup_check_session_logout_and_login(client):
    response = signup(client)
    assert response.status_code == 201
    assert response.get_json()["username"] == "testuser"

    assert client.get("/check_session").get_json()["username"] == "testuser"
    assert client.delete("/logout").status_code == 200
    assert client.get("/check_session").get_json() == {}

    response = client.post("/login", json={"username": "testuser", "password": "password123"})
    assert response.status_code == 200
    assert response.get_json()["username"] == "testuser"


def test_signup_rejects_duplicate_username_and_bad_password_confirmation(client):
    assert signup(client).status_code == 201
    assert signup(client).status_code == 409

    response = client.post(
        "/signup",
        json={"username": "newuser", "password": "password123", "password_confirmation": "different"},
    )
    assert response.status_code == 400
    assert "Password confirmation must match password." in response.get_json()["errors"]


def test_notes_require_authentication(client):
    assert client.get("/notes").status_code == 401
    assert client.post("/notes", json={"title": "No", "content": "Access"}).status_code == 401


def test_authenticated_user_can_complete_note_crud(client):
    signup(client)
    created = create_note(client)
    assert created.status_code == 201
    note_id = created.get_json()["id"]

    assert client.get(f"/notes/{note_id}").get_json()["title"] == "First note"

    updated = client.patch(f"/notes/{note_id}", json={"title": "Updated title"})
    assert updated.status_code == 200
    assert updated.get_json()["title"] == "Updated title"
    assert updated.get_json()["content"] == "A private note"

    assert client.delete(f"/notes/{note_id}").status_code == 204
    assert client.get(f"/notes/{note_id}").status_code == 404


def test_notes_are_paginated_and_hidden_from_other_users(client):
    signup(client, "owner")
    note_id = create_note(client, "One").get_json()["id"]
    create_note(client, "Two")
    create_note(client, "Three")

    page = client.get("/notes?page=2&per_page=2")
    assert page.status_code == 200
    assert page.get_json()["total"] == 3
    assert page.get_json()["pages"] == 2
    assert len(page.get_json()["notes"]) == 1

    client.delete("/logout")
    signup(client, "otheruser")
    assert client.get("/notes").get_json()["notes"] == []
    assert client.get(f"/notes/{note_id}").status_code == 404
    assert client.patch(f"/notes/{note_id}", json={"title": "Stolen"}).status_code == 404
    assert client.delete(f"/notes/{note_id}").status_code == 404
