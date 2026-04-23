"""
Tags CRUD endpoint tests.

Covers:
  - GET    /tags          (200, 401)
  - POST   /tags          (201, 400, 401)
  - GET    /tags/<id>     (200, 404)
  - PATCH  /tags/<id>     (200, 404)
  - DELETE /tags/<id>     (204, 404)
"""


class TestListTags:
    def test_list_tags_returns_200(self, client, alice_token):
        resp = client.get("/tags", headers={"Authorization": f"Bearer {alice_token}"})
        assert resp.status_code == 200
        assert "tags" in resp.get_json()

    def test_list_tags_without_token_returns_401(self, client):
        resp = client.get("/tags")
        assert resp.status_code == 401


class TestCreateTag:
    def test_create_tag_returns_201(self, client, alice_token):
        resp = client.post(
            "/tags",
            json={"name": "Work", "color": "#3B82F6"},
            headers={"Authorization": f"Bearer {alice_token}"},
        )
        assert resp.status_code == 201
        body = resp.get_json()
        assert body["name"] == "Work"
        assert body["color"] == "#3B82F6"

    def test_create_tag_without_token_returns_401(self, client):
        resp = client.post("/tags", json={"name": "Work", "color": "#3B82F6"})
        assert resp.status_code == 401

    def test_create_tag_missing_name_returns_400(self, client, alice_token):
        resp = client.post(
            "/tags",
            json={"color": "#3B82F6"},
            headers={"Authorization": f"Bearer {alice_token}"},
        )
        assert resp.status_code == 400

    def test_create_tag_invalid_color_returns_400(self, client, alice_token):
        resp = client.post(
            "/tags",
            json={"name": "Work", "color": "blue"},
            headers={"Authorization": f"Bearer {alice_token}"},
        )
        assert resp.status_code == 400

    def test_create_duplicate_tag_returns_400(self, client, alice_token, alice_tag):
        resp = client.post(
            "/tags",
            json={"name": "Work", "color": "#FF0000"},
            headers={"Authorization": f"Bearer {alice_token}"},
        )
        assert resp.status_code == 400


class TestGetTag:
    def test_get_own_tag_returns_200(self, client, alice_token, alice_tag):
        resp = client.get(
            f"/tags/{alice_tag.id}",
            headers={"Authorization": f"Bearer {alice_token}"},
        )
        assert resp.status_code == 200

    def test_get_nonexistent_tag_returns_404(self, client, alice_token):
        resp = client.get(
            "/tags/99999",
            headers={"Authorization": f"Bearer {alice_token}"},
        )
        assert resp.status_code == 404

    def test_get_other_users_tag_returns_404(self, client, db, bob, alice_token):
        from app.models.note import Tag
        tag = Tag(user_id=bob.id, name="BobTag", color="#000000")
        db.session.add(tag)
        db.session.commit()
        resp = client.get(
            f"/tags/{tag.id}",
            headers={"Authorization": f"Bearer {alice_token}"},
        )
        assert resp.status_code == 404


class TestUpdateTag:
    def test_update_own_tag_returns_200(self, client, alice_token, alice_tag):
        resp = client.patch(
            f"/tags/{alice_tag.id}",
            json={"color": "#FF0000"},
            headers={"Authorization": f"Bearer {alice_token}"},
        )
        assert resp.status_code == 200
        assert resp.get_json()["color"] == "#FF0000"

    def test_update_nonexistent_tag_returns_404(self, client, alice_token):
        resp = client.patch(
            "/tags/99999",
            json={"name": "X"},
            headers={"Authorization": f"Bearer {alice_token}"},
        )
        assert resp.status_code == 404


class TestDeleteTag:
    def test_delete_own_tag_returns_204(self, client, alice_token, alice_tag):
        resp = client.delete(
            f"/tags/{alice_tag.id}",
            headers={"Authorization": f"Bearer {alice_token}"},
        )
        assert resp.status_code == 204

    def test_delete_nonexistent_tag_returns_404(self, client, alice_token):
        resp = client.delete(
            "/tags/99999",
            headers={"Authorization": f"Bearer {alice_token}"},
        )
        assert resp.status_code == 404
