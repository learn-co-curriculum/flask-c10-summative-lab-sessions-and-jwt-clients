def signup(client, username):
    response = client.post(
        "/signup",
        json={
            "username": username,
            "password": "secret123",
            "password_confirmation": "secret123",
        },
    )
    assert response.status_code == 201
    return response.get_json()


def jwt_headers(user_data):
    return {"Authorization": f"Bearer {user_data['token']}"}


def test_signup_and_login_return_auth_data(client):
    signup_data = signup(client, "alice")

    assert signup_data["user"]["username"] == "alice"
    assert signup_data["token"]

    response = client.post(
        "/login", json={"username": "alice", "password": "secret123"}
    )

    assert response.status_code == 200
    assert response.get_json()["token"]


def test_jwt_logout_requires_a_token(client):
    assert client.delete("/logout").status_code == 401

    user = signup(client, "alice")
    logout = client.delete("/logout", headers=jwt_headers(user))
    assert logout.status_code == 204


def test_unauthorized_users_cannot_access_tasks(client):
    response = client.get("/tasks")

    assert response.status_code == 401
    assert response.get_json() == {"errors": ["Authentication required."]}


def test_users_can_only_manage_their_own_tasks(client):
    alice = signup(client, "alice")
    task_response = client.post(
        "/tasks",
        json={"title": "Private task"},
        headers=jwt_headers(alice),
    )
    task_id = task_response.get_json()["id"]

    bob = signup(client, "bob")
    response = client.get(f"/tasks/{task_id}", headers=jwt_headers(bob))

    assert response.status_code == 404
    assert response.get_json() == {"errors": ["Task not found."]}


def test_task_crud_and_validation(client):
    user = signup(client, "alice")
    headers = jwt_headers(user)

    invalid = client.post("/tasks", json={}, headers=headers)
    assert invalid.status_code == 422

    created = client.post(
        "/tasks", json={"title": "Write tests"}, headers=headers
    )
    assert created.status_code == 201
    task_id = created.get_json()["id"]

    empty_update = client.patch(f"/tasks/{task_id}", json={}, headers=headers)
    assert empty_update.status_code == 422

    updated = client.patch(
        f"/tasks/{task_id}",
        json={"completed": True},
        headers=headers,
    )
    assert updated.status_code == 200
    assert updated.get_json()["completed"] is True

    deleted = client.delete(f"/tasks/{task_id}", headers=headers)
    assert deleted.status_code == 204


def test_task_pagination_and_mutation_ownership(client):
    alice = signup(client, "alice")
    alice_headers = jwt_headers(alice)
    task_ids = []
    for index in range(3):
        response = client.post(
            "/tasks",
            json={"title": f"Task {index}"},
            headers=alice_headers,
        )
        task_ids.append(response.get_json()["id"])

    first_page = client.get(
        "/tasks?page=1&per_page=2", headers=alice_headers
    )
    assert first_page.status_code == 200
    assert len(first_page.get_json()["tasks"]) == 2
    assert first_page.get_json()["has_next"] is True

    bob = signup(client, "bob")
    bob_headers = jwt_headers(bob)
    assert client.patch(
        f"/tasks/{task_ids[0]}",
        json={"title": "Not Alice's task"},
        headers=bob_headers,
    ).status_code == 404
    assert client.delete(
        f"/tasks/{task_ids[0]}", headers=bob_headers
    ).status_code == 404