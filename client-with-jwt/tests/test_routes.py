import pytest
from server.app import app
from server.models import db


# FIXTURES & SETUP

pytest.fixture
def client():
    """Configure a clean in-memory database and test client for each test run."""
    app.config["TESTING"] = True
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    with app.app_context():
        db.create_all()
        yield app.test_client()
        db.session.remove()
        db.drop_all()

#  READ ROUTE TESTS

def test_get_recipes_empty_list(client):
    """Test fetching all recipes when the database is empty returns 200 OK and an empty list."""
    response = client.get("/recipes")
    assert response.status_code == 200
    assert response.get_json() == []

def test_get_recipes_populated(client):
    """Test fetching all recipes returns a populated list of recipes."""
    # Seed data
    client.post("/recipes", json={"title": "Pancakes", "instructions": "Mix and fry."})
    client.post("/recipes", json={"title": "Waffles", "instructions": "Mix and bake in iron."})

    response = client.get("/recipes")
    assert response.status_code == 200
    data = response.get_json()
    assert len(data) == 2
    assert data[0]["title"] == "Pancakes"
    assert data[1]["title"] == "Waffles"

def test_get_single_recipe_success(client):
    """Test fetching a single valid recipe by ID."""
    post_res = client.post("/recipes", json={"title": "Omelette", "instructions": "Whisk eggs and cook."})
    recipe_id = post_res.get_json()["id"]

    response = client.get(f"/recipes/{recipe_id}")
    assert response.status_code == 200
    data = response.get_json()
    assert data["id"] == recipe_id
    assert data["title"] == "Omelette"

def test_get_single_recipe_not_found(client):
    """Test fetching a non-existent recipe ID returns 404 Not Found."""
    response = client.get("/recipes/9999")
    assert response.status_code == 404
    data = response.get_json()
    assert "error" in data or "message" in data


# CREATE ROUTE TESTS

def test_create_recipe_success(client):
    """Test creating a new valid recipe returns 201 Created with saved data."""
    payload = {
        "title": "Avocado Toast",
        "instructions": "Toast bread, smash avocado on top."
    }
    response = client.post("/recipes", json=payload)
    assert response.status_code == 201
    data = response.get_json()
    assert "id" in data
    assert data["title"] == payload["title"]
    assert data["instructions"] == payload["instructions"]

def test_create_recipe_missing_required_fields(client):
    """Test creating a recipe with missing required fields returns 400 Bad Request."""
    payload = {"instructions": "Missing the title field"}
    response = client.post("/recipes", json=payload)
    assert response.status_code == 400
    data = response.get_json()
    assert "error" in data or "message" in data

def test_create_recipe_empty_payload(client):
    """Test creating a recipe with an empty JSON object returns 400 Bad Request."""
    response = client.post("/recipes", json={})
    assert response.status_code == 400


# UPDATE ROUTE TESTS


def test_update_recipe_partial_success(client):
    """Test updating specific fields of a recipe returns 200 OK."""
    post_res = client.post("/recipes", json={"title": "Soup", "instructions": "Boil water."})
    recipe_id = post_res.get_json()["id"]

    patch_payload = {"title": "Vegetable Soup"}
    response = client.patch(f"/recipes/{recipe_id}", json=patch_payload)
    assert response.status_code == 200
    data = response.get_json()
    assert data["title"] == "Vegetable Soup"
    assert data["instructions"] == "Boil water."  # Unchanged field remains intact

def test_update_recipe_not_found(client):
    """Test updating a non-existent recipe ID returns 404 Not Found."""
    response = client.patch("/recipes/9999", json={"title": "Ghost Recipe"})
    assert response.status_code == 404

def test_update_recipe_invalid_data(client):
    """Test updating a recipe with invalid or empty data fields returns 400 Bad Request."""
    post_res = client.post("/recipes", json={"title": "Salad", "instructions": "Chop veggies."})
    recipe_id = post_res.get_json()["id"]

    response = client.patch(f"/recipes/{recipe_id}", json={"title": ""})
    assert response.status_code in [400, 422]


# DELETE ROUTE TESTS

def test_delete_recipe_success(client):
    """Test deleting an existing recipe returns 200 OK or 204 No Content, and removes record."""
    post_res = client.post("/recipes", json={"title": "Temp Recipe", "instructions": "Delete me."})
    recipe_id = post_res.get_json()["id"]

    # Delete the record
    del_response = client.delete(f"/recipes/{recipe_id}")
    assert del_response.status_code in [200, 204]

    # Verify it can no longer be found
    get_response = client.get(f"/recipes/{recipe_id}")
    assert get_response.status_code == 404

def test_delete_recipe_not_found(client):
    """Test deleting a non-existent recipe ID returns 404 Not Found."""
    response = client.delete("/recipes/9999")
    assert response.status_code == 404