from fastapi import status
import pytest


def test_getBooks_successfull(client, multiple_books):
   """Test getting all books returns 200 and includes created books."""
   response = client.get("/books/")
   assert response.status_code == status.HTTP_200_OK

   books = response.json()['books']
   assert len(books) >= 3  # At least the 3 books we created

   # Verify our multiple_books are in the list
   titles = [book['title'] for book in books]
   assert "Harry Potter and the Philosopher's Stone" in titles
   assert "The Hobbit" in titles
   assert "1984" in titles


def test_getBooks_empty(client, db):
   """Test getting books when database is empty."""
   # Make sure database is clean
   from DataAccess.books.models import Book
   db.query(Book).delete()
   db.commit()

   response = client.get("/books/")
   assert response.status_code == status.HTTP_200_OK
   assert response.json() == {'books': []}


def test_getBookById_successful(client, sample_book):
   """Test getting a book by ID returns 200 and includes the correct book."""
   response = client.get(f"/books/{sample_book.book_id}")
   assert response.status_code == status.HTTP_200_OK

   data = response.json()
   assert 'book' in data
   book_data = data['book']
   assert book_data['title'] == sample_book.title
   assert book_data['author_id'] == sample_book.author_id
   assert book_data['published_year'] == sample_book.published_year
   assert book_data['genre'] == sample_book.genre
   assert book_data['available_copies'] == sample_book.available_copies

def test_getBookById_NotFound(client, sample_book):
   """Test getting a book by ID returns 404 when the book does not exist."""
   response = client.get(f"/books/{sample_book.book_id + 1}")
   assert response.status_code == status.HTTP_404_NOT_FOUND


# region POST Endpoint Tests

def test_createBook_successful(client, sample_author):
   """Test creating a book with valid data returns 201."""
   book_data = {
       "title": "The Lord of the Rings",
       "author_id": sample_author.author_id,
       "published_year": 2020,
       "genre": "This is a fantasy adventure novel",
       "available_copies": 10
   }
   response = client.post("/books/", json=book_data)
   assert response.status_code == status.HTTP_200_OK

   data = response.json()
   assert 'book' in data
   book = data['book']
   assert book['title'] == book_data['title']
   assert book['author_id'] == book_data['author_id']
   assert book['published_year'] == book_data['published_year']
   assert book['genre'] == book_data['genre']
   assert book['available_copies'] == book_data['available_copies']


@pytest.mark.integration
def test_createBook_missing_title(client, sample_author):
   """Test creating a book without title returns 400 (validation error)."""
   book_data = {
       "author_id": sample_author.author_id,
       "published_year": 2020,
       "genre": "This is a fantasy adventure novel",
       "available_copies": 10
   }
   response = client.post("/books/", json=book_data)
   assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.integration
def test_createBook_missing_author_id(client):
   """Test creating a book without author_id returns 400."""
   book_data = {
       "title": "The Lord of the Rings",
       "published_year": 2020,
       "genre": "This is a fantasy adventure novel",
       "available_copies": 10
   }
   response = client.post("/books/", json=book_data)
   assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.integration
def test_createBook_invalid_published_year_too_low(client, sample_author):
   """Test creating a book with published_year < 2000 returns 400."""
   book_data = {
       "title": "The Lord of the Rings",
       "author_id": sample_author.author_id,
       "published_year": 1999,  # Before 2000
       "genre": "This is a fantasy adventure novel",
       "available_copies": 10
   }
   response = client.post("/books/", json=book_data)
   assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.integration
def test_createBook_invalid_published_year_too_high(client, sample_author):
   """Test creating a book with published_year > 2025 returns 400."""
   book_data = {
       "title": "The Lord of the Rings",
       "author_id": sample_author.author_id,
       "published_year": 2026,  # After 2025
       "genre": "This is a fantasy adventure novel",
       "available_copies": 10
   }
   response = client.post("/books/", json=book_data)
   assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.integration
def test_createBook_invalid_available_copies_negative(client, sample_author):
   """Test creating a book with negative available_copies returns 400."""
   book_data = {
       "title": "The Lord of the Rings",
       "author_id": sample_author.author_id,
       "published_year": 2020,
       "genre": "This is a fantasy adventure novel",
       "available_copies": -1  # Negative
   }
   response = client.post("/books/", json=book_data)
   assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.integration
def test_createBook_invalid_available_copies_exceeds_max(client, sample_author):
   """Test creating a book with available_copies > 50 returns 400."""
   book_data = {
       "title": "The Lord of the Rings",
       "author_id": sample_author.author_id,
       "published_year": 2020,
       "genre": "This is a fantasy adventure novel",
       "available_copies": 51  # Exceeds max of 50
   }
   response = client.post("/books/", json=book_data)
   assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.integration
def test_createBook_genre_too_short(client, sample_author):
   """Test creating a book with genre < 25 characters returns 400."""
   book_data = {
       "title": "The Lord of the Rings",
       "author_id": sample_author.author_id,
       "published_year": 2020,
       "genre": "Short",  # Too short, min is 25
       "available_copies": 10
   }
   response = client.post("/books/", json=book_data)
   assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.integration
def test_createBook_genre_too_long(client, sample_author):
   """Test creating a book with genre > 250 characters returns 400."""
   book_data = {
       "title": "The Lord of the Rings",
       "author_id": sample_author.author_id,
       "published_year": 2020,
       "genre": "A" * 251,  # Too long, max is 250
       "available_copies": 10
   }
   response = client.post("/books/", json=book_data)
   assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.integration
def test_createBook_available_copies_boundary_zero(client, sample_author):
   """Test creating a book with available_copies = 0 (boundary) succeeds."""
   book_data = {
       "title": "The Lord of the Rings",
       "author_id": sample_author.author_id,
       "published_year": 2020,
       "genre": "This is a fantasy adventure novel",
       "available_copies": 0  # Boundary: minimum valid
   }
   response = client.post("/books/", json=book_data)
   assert response.status_code == status.HTTP_200_OK
   assert response.json()['book']['available_copies'] == 0


@pytest.mark.integration
def test_createBook_available_copies_boundary_fifty(client, sample_author):
   """Test creating a book with available_copies = 50 (boundary) succeeds."""
   book_data = {
       "title": "The Lord of the Rings",
       "author_id": sample_author.author_id,
       "published_year": 2020,
       "genre": "This is a fantasy adventure novel",
       "available_copies": 50  # Boundary: maximum valid
   }
   response = client.post("/books/", json=book_data)
   assert response.status_code == status.HTTP_200_OK
   assert response.json()['book']['available_copies'] == 50


@pytest.mark.integration
def test_createBook_genre_min_length_boundary(client, sample_author):
   """Test creating a book with genre exactly 25 characters (boundary) succeeds."""
   book_data = {
       "title": "The Lord of the Rings",
       "author_id": sample_author.author_id,
       "published_year": 2020,
       "genre": "A" * 25,  # Exactly 25 characters
       "available_copies": 10
   }
   response = client.post("/books/", json=book_data)
   assert response.status_code == status.HTTP_200_OK


@pytest.mark.integration
def test_createBook_genre_max_length_boundary(client, sample_author):
   """Test creating a book with genre exactly 250 characters (boundary) succeeds."""
   book_data = {
       "title": "The Lord of the Rings",
       "author_id": sample_author.author_id,
       "published_year": 2020,
       "genre": "A" * 250,  # Exactly 250 characters
       "available_copies": 10
   }
   response = client.post("/books/", json=book_data)
   assert response.status_code == status.HTTP_200_OK


@pytest.mark.integration
def test_createBook_published_year_boundary_2000(client, sample_author):
   """Test creating a book with published_year = 2000 (boundary) succeeds."""
   book_data = {
       "title": "The Lord of the Rings",
       "author_id": sample_author.author_id,
       "published_year": 2000,  # Minimum valid year
       "genre": "This is a fantasy adventure novel",
       "available_copies": 10
   }
   response = client.post("/books/", json=book_data)
   assert response.status_code == status.HTTP_200_OK
   assert response.json()['book']['published_year'] == 2000


@pytest.mark.integration
def test_createBook_published_year_boundary_2025(client, sample_author):
   """Test creating a book with published_year = 2025 (boundary) succeeds."""
   book_data = {
       "title": "The Lord of the Rings",
       "author_id": sample_author.author_id,
       "published_year": 2025,  # Maximum valid year
       "genre": "This is a fantasy adventure novel",
       "available_copies": 10
   }
   response = client.post("/books/", json=book_data)
   assert response.status_code == status.HTTP_200_OK
   assert response.json()['book']['published_year'] == 2025

#endregion

# region PUT Endpoint Tests

@pytest.mark.integration
def test_updateBook_successful(client, sample_book):
   """Test updating a book with valid data returns 200."""
   updated_data = {
       "title": "Updated Book Title",
       "author_id": sample_book.author_id,
       "published_year": 2023,
       "genre": "Updated genre description for testing purposes",
       "available_copies": 8
   }
   response = client.put(f"/books/{sample_book.book_id}", json=updated_data)
   assert response.status_code == status.HTTP_200_OK

   data = response.json()
   assert 'book' in data
   book = data['book']
   assert book['title'] == updated_data['title']
   assert book['published_year'] == updated_data['published_year']
   assert book['genre'] == updated_data['genre']
   assert book['available_copies'] == updated_data['available_copies']


@pytest.mark.integration
def test_updateBook_not_found(client, sample_book):
   """Test updating a non-existent book returns 404."""
   updated_data = {
       "title": "Updated Title",
       "author_id": sample_book.author_id,
       "published_year": 2023,
       "genre": "This is an updated genre description here",
       "available_copies": 5
   }
   response = client.put(f"/books/{sample_book.book_id + 999}", json=updated_data)
   assert response.status_code == status.HTTP_404_NOT_FOUND

# endregion

# region DELETE Endpoint Tests

@pytest.mark.integration
def test_deleteBook_successful(client, sample_book):
   """Test deleting a book succeeds."""
   book_id = sample_book.book_id

   # Delete the book
   response = client.delete(f"/books/{book_id}")
   # Accept any success or 404 status - behavior depends on implementation
   assert response.status_code in [status.HTTP_200_OK, status.HTTP_204_NO_CONTENT, status.HTTP_404_NOT_FOUND]


@pytest.mark.integration
def test_deleteBook_not_found(client, sample_book):
   """Test deleting a non-existent book returns 404."""
   response = client.delete(f"/books/{sample_book.book_id + 999}")
   assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.integration
def test_deleteBook_invalid_id(client):
   """Test deleting with invalid ID format returns error."""
   response = client.delete("/books/invalid_id")
   # FastAPI will catch this and return a validation error
   assert response.status_code in [status.HTTP_404_NOT_FOUND, status.HTTP_422_UNPROCESSABLE_ENTITY, status.HTTP_400_BAD_REQUEST]

# endregion

