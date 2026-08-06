from server.models import Task, db


def signup(client, username):
    return client.post(
        "/signup",
        json={
            "username": username,
            "password": "password123",
            "password_confirmation": "password123",
        },
    )


def test_task_routes_require_login(client):
    assert client.get("/tasks").status_code == 401

    assert client.post(
        "/tasks",
        json={"title": "Blocked"},
    ).status_code == 401

    assert client.get("/tasks/1").status_code == 401

    assert client.patch(
        "/tasks/1",
        json={"completed": True},
    ).status_code == 401

    assert client.delete("/tasks/1").status_code == 401


def test_user_can_create_task(client):
    signup(client, "create_user")

    response = client.post(
        "/tasks",
        json={
            "title": "Finish project",
            "description": "Build Flask API",
            "completed": False,
        },
    )

    assert response.status_code == 201

    data = response.get_json()

    assert data["title"] == "Finish project"
    assert data["completed"] is False


def test_user_can_get_task(client):
    signup(client, "read_user")

    created = client.post(
        "/tasks",
        json={"title": "Read this task"},
    )

    task_id = created.get_json()["id"]

    response = client.get(f"/tasks/{task_id}")

    assert response.status_code == 200


def test_user_can_update_task(client):
    signup(client, "update_user")

    created = client.post(
        "/tasks",
        json={
            "title": "Original",
            "completed": False,
        },
    )

    task_id = created.get_json()["id"]

    response = client.patch(
        f"/tasks/{task_id}",
        json={
            "title": "Updated",
            "completed": True,
        },
    )

    assert response.status_code == 200
    assert response.get_json()["completed"] is True


def test_user_can_delete_task(client):
    signup(client, "delete_user")

    created = client.post(
        "/tasks",
        json={"title": "Delete this"},
    )

    task_id = created.get_json()["id"]

    response = client.delete(f"/tasks/{task_id}")

    assert response.status_code == 204


def test_user_cannot_access_other_task(client, app):
    signup(client, "owner_user")

    created = client.post(
        "/tasks",
        json={"title": "Private task"},
    )

    task_id = created.get_json()["id"]

    client.delete("/logout")

    signup(client, "other_user")

    assert client.get(f"/tasks/{task_id}").status_code == 404

    assert client.patch(
        f"/tasks/{task_id}",
        json={"completed": True},
    ).status_code == 404

    assert client.delete(f"/tasks/{task_id}").status_code == 404

    with app.app_context():
        task = db.session.get(Task, task_id)

        assert task is not None


def test_index_only_returns_owned_tasks(client):
    signup(client, "first_user")

    client.post(
        "/tasks",
        json={"title": "First task"},
    )

    client.delete("/logout")

    signup(client, "second_user")

    client.post(
        "/tasks",
        json={"title": "Second task"},
    )

    response = client.get("/tasks")

    tasks = response.get_json()["tasks"]

    assert len(tasks) == 1
    assert tasks[0]["title"] == "Second task"


def test_task_index_is_paginated(client):
    signup(client, "pagination_user")

    for number in range(12):
        client.post(
            "/tasks",
            json={"title": f"Task {number + 1}"},
        )

    response = client.get("/tasks?page=1&per_page=5")

    data = response.get_json()

    assert response.status_code == 200
    assert len(data["tasks"]) == 5
    assert data["pagination"]["total_items"] == 12
    assert data["pagination"]["total_pages"] == 3


def test_client_user_id_is_ignored(client):
    signup_response = signup(client, "ownership_user")

    user_id = signup_response.get_json()["id"]

    response = client.post(
        "/tasks",
        json={
            "title": "Owned task",
            "user_id": 9999,
        },
    )

    assert response.status_code == 201
    assert response.get_json()["user_id"] == user_id