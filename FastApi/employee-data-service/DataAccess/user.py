from DataAccess.Database import Base
from sqlalchemy import Column, Integer, String, Boolean, Date, Float  # Add other types as needed
from pydantic import BaseModel, Field
from datetime import date


class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True, index=True)
    UserName = Column(String(15), nullable=False)
    Password = Column(String(15), nullable=False)
    Email = Column(String(50), nullable=False)
    isActive = Column(Boolean, nullable=False, default=True)

class UserModel(BaseModel):
    UserName: str = Field(..., max_length=15)
    Password: str = Field(..., max_length=15)
    Email: str = Field(..., max_length=50) 
    isActive: bool
