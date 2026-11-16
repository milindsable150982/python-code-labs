#SQLAlchemy / SQLModel DB tables

from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import Mapped, mapped_column
from DataAccess.config.database import Base
from sqlalchemy import Date

class Member(Base):
    __tablename__ = "members"

    member_id: Mapped[int] = mapped_column(primary_key=True, index=True, autoincrement=True)
    first_name: Mapped[str] = mapped_column(String(100), index=True)
    last_name: Mapped[str] = mapped_column(String(100), index=True)
    email: Mapped[str] = mapped_column(String(100), index=True)
    join_date: Mapped[Date] = mapped_column(Date, index=True)