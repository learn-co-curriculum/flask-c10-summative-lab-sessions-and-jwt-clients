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


def test_session_status_and_logout_use_auth_status_codes(client):
    unauthenticated = client.get("/check_session")
    assert unauthenticated.status_code == 401

    signup(client, "alice")
    authenticated = client.get("/check_session")
    assert authenticated.status_code == 200

    logout = client.delete("/logout")
    assert logout.status_code == 204
    assert client.get("/check_session").status_code == 401


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