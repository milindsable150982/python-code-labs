#SQLAlchemy / SQLModel DB tables

from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from DataAccess.config.database import Base

class Book(Base):
    __tablename__ = "books"

    book_id: Mapped[int] = mapped_column(primary_key=True, index=True, autoincrement=True)
    title: Mapped[str] = mapped_column(String(200), index=False)
    author_id: Mapped[int] = mapped_column(Integer, ForeignKey("authors.author_id"), index=False)
    published_year: Mapped[int] = mapped_column(Integer, index=False)
    genre: Mapped[str] = mapped_column(String(100), index=False)
    available_copies: Mapped[int] = mapped_column(Integer, index=False)