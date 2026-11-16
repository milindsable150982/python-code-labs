# Pydantic request/response models
from operator import ge
from pydantic import BaseModel, Field

class BookSchema(BaseModel):
    title: str = Field(..., description="Title of the book")
    author_id: int = Field(..., description="Unique identifier for the author of the book")
    published_year: int = Field(..., ge=2000, le=2025, description="Year the book was published")
    available_copies: int = Field(..., ge=0, le=50, description="Number of available copies of the book")
    genre: str = Field(..., max_length=250, min_length=25, description="Genre of the book")