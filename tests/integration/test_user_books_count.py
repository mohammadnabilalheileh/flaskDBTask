def test_user_books_count(client):
    client.post("/users", json={"username": "reader"})

    client.post("/books", json={
        "title": "Book 1",
        "author": "A",
        "library_id": 1
    })

    client.post("/books", json={
        "title": "Book 2",
        "author": "B",
        "library_id": 1
    })

    response = client.get("/users/1/books/count")

    assert response.status_code == 200
    assert response.json["books_count"] == 2
