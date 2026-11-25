from fastapi import status
import pytest
from Test.conftest import db, client


def test_getAuther_successfull(client, multiple_authors):
    """Test getting all authors returns 200 and includes created authors."""
    response = client.get("/authors")
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()['authors']) == 3

def test_getAuthor_by_id_successfull(client, multiple_authors):
    """Test getting an author by ID returns 200 and the correct author."""
    author_id = multiple_authors[0].author_id
    response = client.get(f"/authors/{author_id}")
    author = response.json()['author']
    assert response.status_code == status.HTTP_200_OK
    assert author["author_id"] == author_id

def test_createAuthor_successfull(client):
    response = client.post("/authors", json={"first_name": "John", "last_name": "Doe", "birth_year": 1980})
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert "author" in data
    author = data['author']
    assert author["first_name"] == "John"
    assert author["last_name"] == "Doe"
    assert author["birth_year"] == 1980

def test_updateAuthor_successfull(client, multiple_authors):
    authorId = multiple_authors[0].author_id
    response = client.put(f"/authors/{authorId}", json={"first_name": "Jane", "last_name": "Smith", "birth_year": 1990})
    assert response.status_code == status.HTTP_200_OK
    data = response.json()['author']
    assert data["first_name"] == "Jane"
    assert data["last_name"] == "Smith"
    assert data["birth_year"] == 1990

def test_deleteAuthor_successfull(client, multiple_authors):
    authorId = multiple_authors[0].author_id
    response = client.delete(f"/authors/{authorId}")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["message"] == "Author deleted successfully"
