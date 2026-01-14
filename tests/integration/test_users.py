def test_create_user(client):
    response = client.post("/users", json={"username": "mohammad"})
    assert response.status_code == 201
    assert response.json["username"] == "mohammad"

def test_list_users(client):
    client.post("/users", json={"username": "user1"})
    response = client.get("/users")

    assert response.status_code == 200
    assert len(response.json) == 1

def test_update_user(client):
    client.post("/users", json={"username": "old"})
    response = client.put("/users/1", json={"username": "new"})

    assert response.status_code == 200
    assert response.json["username"] == "new"

def test_delete_user(client):
    client.post("/users", json={"username": "temp"})
    response = client.delete("/users/1")

    assert response.status_code == 204
