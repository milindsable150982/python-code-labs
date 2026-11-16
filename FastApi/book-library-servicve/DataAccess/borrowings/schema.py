# Pydantic request/response models

from pydantic import BaseModel, Field
from datetime import date

class BorrowingSchema(BaseModel):
    book_id: int = Field(..., description="ID of the book being borrowed")
    member_id: int = Field(..., description="ID of the member borrowing the book")