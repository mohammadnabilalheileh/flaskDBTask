def setup_user_and_library(client):
    client.post("/users", json={"username": "owner"})

def test_create_book(client):
    setup_user_and_library(client)

    response = client.post("/books", json={
        "title": "1984",
        "author": "Orwell",
        "library_id": 1
    })

    assert response.status_code == 201
    assert response.json["title"] == "1984"

def test_delete_book(client):
    setup_user_and_library(client)

    client.post("/books", json={
        "title": "Temp",
        "author": "Test",
        "library_id": 1
    })

    response = client.delete("/books/1")
    assert response.status_code == 204
