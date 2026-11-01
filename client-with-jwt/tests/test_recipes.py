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

    # GET /recipes 
    get_all_res = client.get('/recipes')
    assert get_all_res.status_code == 200
    assert len(get_all_res.get_json()["recipes"]) == 1

    # GET /recipes/<id> 
    get_one_res = client.get(f'/recipes/{recipe_id}')
    assert get_one_res.status_code == 200
    assert get_one_res.get_json()["title"] == "Pancakes"


    # PATCH /recipes/<id>
    patch_res = client.patch(f'/recipes/{recipe_id}', json={
        "title": "Fluffy Pancakes"
    })
    assert patch_res.status_code == 200
    assert patch_res.get_json()["title"] == "Fluffy Pancakes"

    # DELETE /recipes/<id>
    delete_res = client.delete(f'/recipes/{recipe_id}')
    assert delete_res.status_code == 204

    # Verify it's gone
    verify_delete = client.get(f'/recipes/{recipe_id}')
    assert verify_delete.status_code == 404
