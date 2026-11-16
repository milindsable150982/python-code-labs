 # SQLAlchemy / SQLModel DB tables
 
from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from DataAccess.config.database import Base

class Borrowing(Base):
    __tablename__ = "borrowings"

    borrow_id: Mapped[int] = mapped_column(primary_key=True, index=True, autoincrement=True)
    book_id: Mapped[int] = mapped_column(Integer, ForeignKey("books.book_id"), index=False)
    member_id: Mapped[int] = mapped_column(Integer, ForeignKey("members.member_id"), index=False)
    borrow_date: Mapped[Date] = mapped_column(Date, index=False)
    return_date: Mapped[Date] = mapped_column(Date, index=False, nullable=True)