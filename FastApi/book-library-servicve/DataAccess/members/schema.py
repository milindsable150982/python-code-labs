# Pydantic request/response models

from pydantic import BaseModel, Field
from datetime import date

class MemberSchema(BaseModel):
    first_name: str = Field(..., max_length=25, min_length=2, description="First name of the member")
    last_name: str = Field(..., max_length=25, min_length=2, description="Last name of the member")
    email: str = Field(..., max_length=100, description="Email address of the member")
    join_date: date = Field(..., description="Date when the member joined")