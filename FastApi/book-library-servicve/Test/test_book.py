from fastapi.testclient import TestClient 
from main import app
from fastapi import status

client = TestClient(app)

def test_getBooks_successfull():
   response = client.get("/books/")
   assert response.status_code == status.HTTP_200_OK
   assert response.json() == {'books': []}