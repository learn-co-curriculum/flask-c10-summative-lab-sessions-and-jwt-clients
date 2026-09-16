import pytest

from app import app, db
from models import User, Note


@pytest.fixture
def client():
    app.config.update(
        TESTING=True,
        SQLALCHEMY_DATABASE_URI="sqlite://",
        JWT_SECRET_KEY="test-secret-key",
    )
    with app.app_context():
        db.create_all()
        yield app.test_client()
        db.session.remove()
        db.drop_all()


def test_signup_and_me_flow(client):
    response = client.post(
        "/signup",
        json={
            "username": "alice",
            "password": "password123",
            "password_confirmation": "password123",
        },
    )
    assert response.status_code == 201
    payload = response.get_json()
    assert payload["user"]["username"] == "alice"
    assert "token" in payload

    me = client.get(
        "/me",
        headers={"Authorization": f"Bearer {payload['token']}"},
    )
    assert me.status_code == 200
    assert me.get_json()["username"] == "alice"


def test_notes_are_user_owned_and_paginated(client):
    first = client.post(
        "/signup",
        json={
            "username": "firstuser",
            "password": "password123",
            "password_confirmation": "password123",
        },
    )
    second = client.post(
        "/signup",
        json={
            "username": "seconduser",
            "password": "password123",
            "password_confirmation": "password123",
        },
    )

    token_one = first.get_json()["token"]
    token_two = second.get_json()["token"]

    note_response = client.post(
        "/notes",
        json={"title": "First note", "content": "Hello", "category": "Tasks"},
        headers={"Authorization": f"Bearer {token_one}"},
    )
    assert note_response.status_code == 201
    assert note_response.get_json()["category"] == "Tasks"

    list_response = client.get(
        "/notes?page=1&per_page=10",
        headers={"Authorization": f"Bearer {token_one}"},
    )
    assert list_response.status_code == 200
    assert list_response.get_json()["items"][0]["title"] == "First note"
    assert list_response.get_json()["items"][0]["category"] == "Tasks"

    filtered_response = client.get(
        "/notes?category=Tasks",
        headers={"Authorization": f"Bearer {token_one}"},
    )
    assert filtered_response.status_code == 200
    assert filtered_response.get_json()["items"][0]["category"] == "Tasks"

    other_users_notes = client.get(
        "/notes",
        headers={"Authorization": f"Bearer {token_two}"},
    )
    assert other_users_notes.status_code == 200
    assert other_users_notes.get_json()["items"] == []

    update_response = client.patch(
        f"/notes/{note_response.get_json()['id']}",
        json={"content": "Updated content"},
        headers={"Authorization": f"Bearer {token_one}"},
    )
    assert update_response.status_code == 200
    assert update_response.get_json()["content"] == "Updated content"

    unauthorized_update = client.patch(
        f"/notes/{note_response.get_json()['id']}",
        json={"content": "Not allowed"},
        headers={"Authorization": f"Bearer {token_two}"},
    )
    assert unauthorized_update.status_code == 403

    delete_response = client.delete(
        f"/notes/{note_response.get_json()['id']}",
        headers={"Authorization": f"Bearer {token_one}"},
    )
    assert delete_response.status_code == 200
