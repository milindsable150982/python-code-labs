import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from fastapi.testclient import TestClient
from main import app
from DataAccess.config.database import get_db, Base
from DataAccess.books.models import Book
from DataAccess.authors.models import Author
from datetime import date  # ← Add this import
from DataAccess.members.models import Member
from DataAccess.borrowings.models import Borrowing

# Test Database Setup
TEST_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(
    TEST_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)

# Create all tables
Base.metadata.create_all(bind=engine)
TestSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    """Override the get_db dependency for testing."""
    db = TestSessionLocal()
    try:
        yield db
    finally:
        db.close()


# Override dependency before app starts
app.dependency_overrides[get_db] = override_get_db

@pytest.fixture
def db():
    """
    Provide a test database session with transaction rollback for isolation.
    Each test gets a clean database state.
    """
    connection = engine.connect()
    transaction = connection.begin()
    session = TestSessionLocal(bind=connection)

    yield session

    session.close()
    transaction.rollback()
    connection.close()


@pytest.fixture
def client():
    """Provide FastAPI test client."""
    return TestClient(app)


@pytest.fixture
def sample_author(db):
    """Create a sample author for testing."""
    author = Author(first_name="J.K.", last_name="Rowling", birth_year=1965)
    db.add(author)
    db.commit()
    db.refresh(author)
    return author


@pytest.fixture
def sample_member(db):
    """Create a sample member for testing."""
    member = Member(first_name="John", last_name="Doe", email="john.doe@example.com")
    db.add(member)
    db.commit()
    db.refresh(member)
    return member


@pytest.fixture
def sample_borrow(db, sample_member, sample_book):
    """Create a sample borrow record for testing."""
    # This fixture would create a sample borrow record
    borrow = Borrowing(member_id=sample_member.member_id, book_id=sample_book.book_id)
    db.add(borrow)
    db.commit()
    db.refresh(borrow)
    return borrow

@pytest.fixture
def sample_book(db, sample_author):
    """Create a sample book for testing."""
    book = Book(
        title="Harry Potter and the Philosopher's Stone",
        author_id=sample_author.author_id,
        published_year=1997,
        genre="Fantasy",
        available_copies=5,
    )
    db.add(book)
    db.commit()
    db.refresh(book)
    return book

@pytest.fixture
def multiple_books(db, sample_author):
    """Create multiple sample books for testing."""
    books = [
        Book(
            title="Harry Potter and the Philosopher's Stone",
            author_id=sample_author.author_id,
            published_year=1997,
            genre="Fantasy",
            available_copies=5,
        ),
        Book(
            title="The Hobbit",
            author_id=sample_author.author_id,
            published_year=1937,
            genre="Fantasy",
            available_copies=3,
        ),
        Book(
            title="1984",
            author_id=sample_author.author_id,
            published_year=1949,
            genre="Dystopian",
            available_copies=2,
        ),
    ]
    db.add_all(books)
    db.commit()
    for book in books:
        db.refresh(book)
    return books


@pytest.fixture
def multiple_members(db, sample_author):
    """Create multiple sample members for testing."""
    members = [
        Member(first_name="John", last_name="Doe", email="john.doe@example.com", join_date=date(2023, 1, 1)),
        Member(first_name="Jane", last_name="Smith", email="jane.smith@example.com", join_date=date(2023, 4, 2)),
        Member(first_name="Bob", last_name="Johnson", email="bob.johnson@example.com", join_date=date(2023, 1, 8)),
    ]
    db.add_all(members)
    db.commit()
    for member in members:
        db.refresh(member)
    return members
