# Pydantic request/response models

from unittest.util import _MAX_LENGTH
from pydantic import BaseModel, Field

class AuthorSchema(BaseModel):
    
    first_name: str = Field(..., max_length=100, min_length=2, description="First Name of the auther")
    last_name: str = Field(..., max_length=100, min_length=2, description="Last Name of the auther")
    birth_year: int = Field(..., ge=1900, le=2010, description="Birth year of the auther")