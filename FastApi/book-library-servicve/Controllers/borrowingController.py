from fastapi import FastAPI, APIRouter, Depends, HTTPException
from DataAccess.borrowings.schema import BorrowingSchema
from DataAccess.config.database import get_db
from DataAccess.borrowings.models import Borrowing
from DataAccess.books.models import Book
from DataAccess.config.database import SessionLocal, engine
from sqlalchemy.exc import SQLAlchemyError
from datetime import date
from authentication.auth_token import verify_token

route = APIRouter()

router = APIRouter(
    prefix="/borrowings",
    tags=["borrowings"],
    dependencies=[Depends(verify_token)],
     responses={404: {"description": "Not found"}, 
               401: {"description": "Unauthorized"}, 
               402: {"description": "Payment Required"},
               400: {"description": "Bad Request"},
               500: {"description": "Internal Server Error"},
               501: {"description": "Not Implemented"}
               }
)
Session = SessionLocal()

@router.get("/")
async def getBorrowings(db=Depends(get_db)):
 return db.query(Borrowing).all()


@router.get("/{id}")
async def getBorrowing(id: int, db=Depends(get_db)):
    borrowing = db.query(Borrowing).filter(Borrowing.borrow_id == id).first()
    if not borrowing:
        raise HTTPException(status_code=404, detail="Borrowing not found")
    return borrowing

@router.post("/")
async def BorrowBook(borrowing: BorrowingSchema):
     try:
        new_borrowing = Borrowing(
            book_id=borrowing.book_id,
            member_id=borrowing.member_id,
            borrow_date=date.today()
        )
        Session.add(new_borrowing)

        book = Session.query(Book).filter(Book.book_id == borrowing.book_id).first()
        book.available_copies = book.available_copies - 1
        Session.commit()

     except SQLAlchemyError as e:
        Session.rollback()  # Reverts both the insert and the update
        raise HTTPException(status_code=500, detail="An error occurred while processing the borrowing request.")
     finally:
         Session.close()

     return new_borrowing

@router.put("/")
async def ReturnBook(borrowing: BorrowingSchema):
     try:

        borrowingRecord = (
            Session.query(Borrowing)
            .filter(
            Borrowing.book_id == borrowing.book_id,
            Borrowing.member_id == borrowing.member_id
            )
         .first()
            )
        borrowingRecord.return_date = date.today()
        Session.commit()
        book = Session.query(Book).filter(Book.book_id == borrowing.book_id).first()
        book.available_copies = book.available_copies + 1
        Session.commit()

     except SQLAlchemyError as e:
        Session.rollback()  # Reverts both the insert and the update
        raise HTTPException(status_code=500, detail="An error occurred while processing the borrowing request.")
     finally:
         Session.close()

     return borrowingRecord

@router.delete("/{id}")
async def deleteBorrowing(id: int, db=Depends(get_db)):
    borrowing = db.query(Borrowing).filter(Borrowing.borrow_id == id).first()
    if not borrowing:
        raise HTTPException(status_code=404, detail="Borrowing not found")
    
    db.delete(borrowing)
    db.commit()
    return {"message": "Borrowing deleted successfully"}