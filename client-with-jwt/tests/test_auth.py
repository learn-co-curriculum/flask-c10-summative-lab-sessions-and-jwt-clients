def test_home(client):
    response = client.get('/')
    assert response.status_code == 200
    assert response.get_json() == {"message": "Welcome to the Recipe Planner API!"}


def test_signup(client):
    response = client.post('/signup', json={
        "username": "chef_test",
        "password": "password123"
    })
    assert response.status_code == 201
    data = response.get_json()
    assert data["username"] == "chef_test"
    assert "id" in data


def test_login_and_check_session(client):
    # First sign up a user
    client.post('/signup', json={
        "username": "chef_test",
        "password": "password123"
    })

    # Test login
    response = client.post('/login', json={
        "username": "chef_test",
        "password": "password123"
    })
    assert response.status_code == 200
    assert response.get_json()["username"] == "chef_test"

    # Test check session
    session_response = client.get('/check_session')
    assert session_response.status_code == 200
    assert session_response.get_json()["username"] == "chef_test"


def test_logout(client):
    # Signup & Login
    client.post('/signup', json={
        "username": "chef_test",
        "password": "password123"
    })
    client.post('/login', json={
        "username": "chef_test",
        "password": "password123"
    })

    # Test logout
    response = client.delete('/logout')
    assert response.status_code == 204

    # Verify session is cleared
    check = client.get('/check_session')
    assert check.status_code == 401
