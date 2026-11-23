from fastapi import FastAPI, APIRouter, Depends, HTTPException
from DataAccess.config.database import get_db
from DataAccess.books.models import Book
from DataAccess.books.schema import BookSchema
from authentication.auth_token import verify_token

route = APIRouter()

router = APIRouter(
    prefix="/books",
    tags=["books"],
   dependencies=[Depends(verify_token)],
    responses={404: {"description": "Not found"}, 
               401: {"description": "Unauthorized"}, 
               402: {"description": "Payment Required"},
               400: {"description": "Bad Request"},
               500: {"description": "Internal Server Error"},
               501: {"description": "Not Implemented"}
               }
)



@router.get("/")
async def getBooks(db=Depends(get_db)):
    books = db.query(Book).all()
    return {"books": books}

@router.get("/{id}")
async def getBook(id: int, db=Depends(get_db)):
    book = db.query(Book).filter(Book.book_id == id).first()
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return {"book": book}


@router.post("/")
async def createBook(book: BookSchema, db=Depends(get_db)):
    new_book = Book(
        title=book.title,
        author_id=book.author_id,
        published_year=book.published_year,
        genre=book.genre,
        available_copies=book.available_copies
    )
    db.add(new_book)
    db.commit()
    db.refresh(new_book)
    return {"book": new_book}

@router.put("/{id}")
async def updateBook(id: int, book_data: BookSchema, db=Depends(get_db)):
    book = db.query(Book).filter(Book.book_id == id).first()
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    book.title = book_data.title
    book.author_id = book_data.author_id
    book.published_year = book_data.published_year
    book.genre = book_data.genre
    book.available_copies = book_data.available_copies
    db.commit()
    db.refresh(book)
    return {"book": book}

@router.delete("/{id}")
async def deleteBook(id: int, db=Depends(get_db)):
    book = db.query(Book).filter(Book.book_id == id).first()
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    db.delete(book)
    db.commit()
    return {"message": "Book deleted successfully"}