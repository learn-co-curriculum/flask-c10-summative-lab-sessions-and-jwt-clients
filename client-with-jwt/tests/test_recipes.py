def test_recipe_crud(client):
    # Attempt to access recipes unauthorized
    res = client.get('/recipes')
    assert res.status_code == 401

    #  Signup and log in
    client.post('/signup', json={
        "username": "chef_test",
        "password": "password123"
    })
    client.post('/login', json={
        "username": "chef_test",
        "password": "password123"
    })
    
# POST /recipes 
    create_res = client.post('/recipes', json={
        "title": "Pancakes",
        "instructions": "Mix flour, milk, and eggs. Cook on skillet.",
        "prep_time_minutes": 15,
        "ingredients": "Flour, Milk, Eggs",
        "is_favorite": True
    })
    assert create_res.status_code == 201
    recipe_data = create_res.get_json()
    recipe_id = recipe_data["id"]
    assert recipe_data["title"] == "Pancakes"
