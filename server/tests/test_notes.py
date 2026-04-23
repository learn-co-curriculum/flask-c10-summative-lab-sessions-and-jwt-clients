"""
Notes CRUD endpoint tests.

Covers:
  - GET    /notes          (200, pagination, 401 without token)
  - POST   /notes          (201, 400 on validation, 401 without token)
  - GET    /notes/<id>     (200, 404 for missing/other-user's note)
  - PATCH  /notes/<id>     (200, 404, 401)
  - DELETE /notes/<id>     (204, 404, 401)
  - Ownership enforcement  (user cannot access another user's notes)
"""


class TestListNotes:
    """GET /notes"""

    def test_list_notes_returns_200(self, client, alice_token):
        resp = client.get(
            "/notes", headers={"Authorization": f"Bearer {alice_token}"}
        )
        assert resp.status_code == 200
        body = resp.get_json()
        assert "notes" in body
        assert "total" in body
        assert "pages" in body
        assert "current_page" in body

    def test_list_notes_without_token_returns_401(self, client):
        resp = client.get("/notes")
        assert resp.status_code == 401

    def test_list_notes_pagination(self, client, db, alice, alice_token):
        from app.models.note import Note
        for i in range(15):
            db.session.add(Note(user_id=alice.id, title=f"Note {i}", content="Body"))
        db.session.commit()

        resp = client.get(
            "/notes?page=1&per_page=5",
            headers={"Authorization": f"Bearer {alice_token}"},
        )
        assert resp.status_code == 200
        body = resp.get_json()
        assert len(body["notes"]) == 5
        assert body["total"] == 15
        assert body["pages"] == 3

    def test_list_notes_only_returns_own_notes(self, client, db, alice, bob, alice_token):
        from app.models.note import Note
        db.session.add(Note(user_id=bob.id, title="Bob's Note", content="Bob's content"))
        db.session.commit()

        resp = client.get(
            "/notes", headers={"Authorization": f"Bearer {alice_token}"}
        )
        body = resp.get_json()
        for note in body["notes"]:
            assert note["user_id"] == alice.id


class TestCreateNote:
    """POST /notes"""

    def test_create_note_returns_201(self, client, alice_token):
        resp = client.post(
            "/notes",
            json={"title": "Test Note", "content": "Test content"},
            headers={"Authorization": f"Bearer {alice_token}"},
        )
        assert resp.status_code == 201
        body = resp.get_json()
        assert body["title"] == "Test Note"

    def test_create_note_without_token_returns_401(self, client):
        resp = client.post(
            "/notes", json={"title": "Test", "content": "Body"}
        )
        assert resp.status_code == 401

    def test_create_note_missing_title_returns_400(self, client, alice_token):
        resp = client.post(
            "/notes",
            json={"content": "No title here"},
            headers={"Authorization": f"Bearer {alice_token}"},
        )
        assert resp.status_code == 400

    def test_create_note_missing_content_returns_400(self, client, alice_token):
        resp = client.post(
            "/notes",
            json={"title": "No content"},
            headers={"Authorization": f"Bearer {alice_token}"},
        )
        assert resp.status_code == 400


class TestGetNote:
    """GET /notes/<id>"""

    def test_get_own_note_returns_200(self, client, alice_token, alice_note):
        resp = client.get(
            f"/notes/{alice_note.id}",
            headers={"Authorization": f"Bearer {alice_token}"},
        )
        assert resp.status_code == 200
        assert resp.get_json()["id"] == alice_note.id

    def test_get_nonexistent_note_returns_404(self, client, alice_token):
        resp = client.get(
            "/notes/99999",
            headers={"Authorization": f"Bearer {alice_token}"},
        )
        assert resp.status_code == 404

    def test_get_other_users_note_returns_404(self, client, db, bob, alice_token):
        from app.models.note import Note
        note = Note(user_id=bob.id, title="Bob's", content="Private")
        db.session.add(note)
        db.session.commit()

        resp = client.get(
            f"/notes/{note.id}",
            headers={"Authorization": f"Bearer {alice_token}"},
        )
        assert resp.status_code == 404


class TestUpdateNote:
    """PATCH /notes/<id>"""

    def test_update_own_note_returns_200(self, client, alice_token, alice_note):
        resp = client.patch(
            f"/notes/{alice_note.id}",
            json={"title": "Updated Title"},
            headers={"Authorization": f"Bearer {alice_token}"},
        )
        assert resp.status_code == 200
        assert resp.get_json()["title"] == "Updated Title"

    def test_update_other_users_note_returns_404(self, client, db, bob, alice_token):
        from app.models.note import Note
        note = Note(user_id=bob.id, title="Bob's", content="Private")
        db.session.add(note)
        db.session.commit()

        resp = client.patch(
            f"/notes/{note.id}",
            json={"title": "Hacked"},
            headers={"Authorization": f"Bearer {alice_token}"},
        )
        assert resp.status_code == 404

    def test_update_without_token_returns_401(self, client, alice_note):
        resp = client.patch(f"/notes/{alice_note.id}", json={"title": "X"})
        assert resp.status_code == 401


class TestDeleteNote:
    """DELETE /notes/<id>"""

    def test_delete_own_note_returns_204(self, client, alice_token, alice_note):
        resp = client.delete(
            f"/notes/{alice_note.id}",
            headers={"Authorization": f"Bearer {alice_token}"},
        )
        assert resp.status_code == 204

    def test_delete_nonexistent_note_returns_404(self, client, alice_token):
        resp = client.delete(
            "/notes/99999",
            headers={"Authorization": f"Bearer {alice_token}"},
        )
        assert resp.status_code == 404

    def test_delete_other_users_note_returns_404(self, client, db, bob, alice_token):
        from app.models.note import Note
        note = Note(user_id=bob.id, title="Bob's", content="Private")
        db.session.add(note)
        db.session.commit()

        resp = client.delete(
            f"/notes/{note.id}",
            headers={"Authorization": f"Bearer {alice_token}"},
        )
        assert resp.status_code == 404
