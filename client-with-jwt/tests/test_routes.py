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
