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
