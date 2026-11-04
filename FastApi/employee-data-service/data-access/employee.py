from Database import Base
from sqlalchemy import Column, Integer, String, Boolean, Date, Float  # Add other types as needed
from pydantic import BaseModel, Field
from datetime import date


class Employee(Base):
    __tablename__ = "employee"

    id = Column(Integer, primary_key=True, index=True)
    FirstName = Column(String(15), nullable=False)
    LastName = Column(String(15), nullable=False)
    Address1 = Column(String(100), nullable=False)
    Address2 = Column(String(100), nullable=True)
    City = Column(String(50), nullable=False)
    State = Column(String(15), nullable=False)
    Zip = Column(String(6), nullable=False)
    Country = Column(String(50), nullable=False)
    IsContract = Column(Boolean, nullable=False, default=False)
    Position = Column(String(50), nullable=False)
    Salary = Column(Float, nullable=False)
    DateOfJoining = Column(Date, nullable=False)


class EmployeeModel(BaseModel):
    FirstName: str = Field(..., max_length=15)
    LastName: str = Field(..., max_length=15)
    Address1: str = Field(..., max_length=100)
    Address2: str = Field(None, max_length=100)
    City: str = Field(..., max_length=50)
    State: str = Field(..., max_length=15)
    Zip: str = Field(..., max_length=6)
    Country: str = Field(..., max_length=50)
    IsContract: bool = Field(default=False)
    Position: str = Field(..., max_length=50)
    Salary: float = Field(..., gt=0)
    DateOfJoining: date