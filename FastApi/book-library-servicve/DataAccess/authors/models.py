#SQLAlchemy / SQLModel DB tables

from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import Mapped, mapped_column
from DataAccess.config.database import Base

class Author(Base):
    __tablename__ = "authors"

    author_id: Mapped[int] = mapped_column(primary_key=True, index=True, autoincrement=True)
    first_name: Mapped[str] = mapped_column(String(100), index=True)
    last_name: Mapped[str] = mapped_column(String(100), index=True)
    birth_year: Mapped[int] = mapped_column(Integer, index=True)