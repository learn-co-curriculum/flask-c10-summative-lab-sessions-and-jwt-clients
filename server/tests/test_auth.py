"""
Authentication endpoint tests.

Covers:
  - POST /signup  (201, 400 on duplicate, 400 on validation errors)
  - POST /login   (200, 401 on bad credentials)
  - GET  /me      (200 with valid token, 401 without token)
"""

import json


class TestSignup:
    """POST /signup"""

    def test_signup_success_returns_201_with_token_and_user(self, client):
        resp = client.post(
            "/signup",
            json={
                "username": "newuser@example.com",
                "password": "password123",
                "password_confirmation": "password123",
            },
        )
        assert resp.status_code == 201
        body = resp.get_json()
        assert "token" in body
        assert body["user"]["username"] == "newuser@example.com"
        assert "id" in body["user"]

    def test_signup_duplicate_username_returns_400(self, client, alice):
        resp = client.post(
            "/signup",
            json={
                "username": "alice@example.com",
                "password": "password123",
                "password_confirmation": "password123",
            },
        )
        assert resp.status_code == 400

    def test_signup_password_mismatch_returns_400(self, client):
        resp = client.post(
            "/signup",
            json={
                "username": "someone",
                "password": "password123",
                "password_confirmation": "different",
            },
        )
        assert resp.status_code == 400

    def test_signup_short_password_returns_400(self, client):
        resp = client.post(
            "/signup",
            json={
                "username": "someone",
                "password": "short",
                "password_confirmation": "short",
            },
        )
        assert resp.status_code == 400

    def test_signup_missing_username_returns_400(self, client):
        resp = client.post(
            "/signup",
            json={
                "password": "password123",
                "password_confirmation": "password123",
            },
        )
        assert resp.status_code == 400


class TestLogin:
    """POST /login"""

    def test_login_success_returns_200_with_token(self, client, alice):
        resp = client.post(
            "/login", json={"username": "alice@example.com", "password": "password123"}
        )
        assert resp.status_code == 200
        body = resp.get_json()
        assert "token" in body
        assert body["user"]["username"] == "alice@example.com"

    def test_login_wrong_password_returns_401(self, client, alice):
        resp = client.post(
            "/login",
            json={"username": "alice@example.com", "password": "wrongpassword"},
        )
        assert resp.status_code == 401

    def test_login_unknown_username_returns_401(self, client):
        resp = client.post(
            "/login", json={"username": "nobody@example.com", "password": "password123"}
        )
        assert resp.status_code == 401

    def test_login_missing_fields_returns_400(self, client):
        resp = client.post("/login", json={"username": "alice@example.com"})
        assert resp.status_code == 400


class TestMe:
    """GET /me"""

    def test_me_with_valid_token_returns_200(self, client, alice, alice_token):
        resp = client.get("/me", headers={"Authorization": f"Bearer {alice_token}"})
        assert resp.status_code == 200
        body = resp.get_json()
        assert body["username"] == "alice@example.com"
        assert body["id"] == alice.id

    def test_me_without_token_returns_401(self, client):
        resp = client.get("/me")
        assert resp.status_code == 401

    def test_me_with_invalid_token_returns_401(self, client):
        resp = client.get("/me", headers={"Authorization": "Bearer not-a-real-token"})
        assert resp.status_code == 401
