def test_transfer_book(client):
    client.post("/users", json={"username": "u1"})
    client.post("/users", json={"username": "u2"})

    client.post("/books", json={
        "title": "Clean Code",
        "author": "Martin",
        "library_id": 1
    })

    response = client.post("/books/1/transfer", json={
        "from_library_id": 1,
        "to_library_id": 2
    })

    assert response.status_code == 200