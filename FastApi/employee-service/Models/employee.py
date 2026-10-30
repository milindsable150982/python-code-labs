from datetime import date
from typing import Optional
from pydantic import BaseModel, Field

class Employee(BaseModel):
    id: Optional[int] = None
    firstname: str = Field(..., min_length=1, max_length=15)
    lastname: str = Field(..., min_length=1, max_length=15)
    address: str = Field(..., min_length=5, max_length=100)
    state: str = Field(..., min_length=1, max_length=15)
    zip: str = Field(..., min_length=1, max_length=6)
    country: str = Field(..., min_length=1, max_length=50)
    position: str = Field(..., min_length=1, max_length=50)
    salary: float = Field(..., ge=0)
    joiningDate: date = Field(..., description="The date the employee joined the company", ge=date(2012, 1, 1), le=date.today())


    model_config = {   
       "json_schema_extra":{
           "example": {
                "firstname": "John",
                "lastname": "Doe",
                "address": "123 Main St",
                "state": "CA",
                "zip": "12345",
                "country": "USA",
                "position": "Software Engineer",
                "salary": 75000.00,
                "joiningDate": "2022-01-01"
            }
           }
        }
