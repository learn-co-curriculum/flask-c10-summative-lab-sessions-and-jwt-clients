from server.models import (
    User,
    db,
)


def test_signup_creates_user(
    client,
    app,
):
    response = client.post(
        "/signup",
        json={
            "username": "new_user",
            "password": "password123",
            "password_confirmation": (
                "password123"
            ),
        },
    )

    assert response.status_code == 201

    data = response.get_json()

    assert "id" in data
    assert data["username"] == "new_user"
    assert "password" not in data
    assert "_password_hash" not in data

    with app.app_context():
        user = (
            User.query.filter_by(
                username="new_user"
            ).first()
        )

        assert user is not None


def test_signup_hashes_password(
    client,
    app,
):
    plain_password = "password123"

    response = client.post(
        "/signup",
        json={
            "username": "secure_user",
            "password": plain_password,
            "password_confirmation": (
                plain_password
            ),
        },
    )

    assert response.status_code == 201

    with app.app_context():
        user = (
            User.query.filter_by(
                username="secure_user"
            ).first()
        )

        assert user is not None
        assert (
            user._password_hash
            != plain_password
        )
        assert (
            user.authenticate(
                plain_password
            )
            is True
        )


def test_signup_logs_user_in(client):
    client.post(
        "/signup",
        json={
            "username": "session_user",
            "password": "password123",
            "password_confirmation": (
                "password123"
            ),
        },
    )

    response = client.get(
        "/check_session"
    )

    assert response.status_code == 200
    assert (
        response.get_json()["username"]
        == "session_user"
    )


def test_signup_rejects_mismatch(
    client,
):
    response = client.post(
        "/signup",
        json={
            "username": "new_user",
            "password": "password123",
            "password_confirmation": (
                "different123"
            ),
        },
    )

    assert response.status_code == 400

    assert response.get_json() == {
        "error": (
            "Passwords do not match."
        )
    }


def test_signup_rejects_duplicate(
    client,
):
    payload = {
        "username": "duplicate_user",
        "password": "password123",
        "password_confirmation": (
            "password123"
        ),
    }

    first_response = client.post(
        "/signup",
        json=payload,
    )

    second_response = client.post(
        "/signup",
        json=payload,
    )

    assert (
        first_response.status_code
        == 201
    )

    assert (
        second_response.status_code
        == 409
    )


def test_login_success(
    client,
    app,
):
    with app.app_context():
        user = User(
            username="login_user"
        )

        user.password = "password123"

        db.session.add(user)
        db.session.commit()

    response = client.post(
        "/login",
        json={
            "username": "login_user",
            "password": "password123",
        },
    )

    assert response.status_code == 200

    assert (
        response.get_json()["username"]
        == "login_user"
    )


def test_invalid_login_returns_401(
    client,
):
    response = client.post(
        "/login",
        json={
            "username": "missing_user",
            "password": "wrongpassword",
        },
    )

    assert response.status_code == 401


def test_logout_clears_session(client):
    client.post(
        "/signup",
        json={
            "username": "logout_user",
            "password": "password123",
            "password_confirmation": (
                "password123"
            ),
        },
    )

    logout_response = client.delete(
        "/logout"
    )

    assert (
        logout_response.status_code
        == 200
    )

    session_response = client.get(
        "/check_session"
    )

    assert session_response.get_json() == {}