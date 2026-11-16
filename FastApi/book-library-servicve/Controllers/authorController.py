from fastapi import FastAPI, APIRouter, Depends, HTTPException
from DataAccess.config.database import get_db
from DataAccess.authors.models import Author
from DataAccess.authors.schema import AuthorSchema
router = APIRouter()

router = APIRouter(
    prefix="/authors",
    tags=["authors"],
    #dependencies=[Depends(get_token_header)],
     responses={404: {"description": "Not found"}, 
               401: {"description": "Unauthorized"}, 
               402: {"description": "Payment Required"},
               400: {"description": "Bad Request"},
               500: {"description": "Internal Server Error"},
               501: {"description": "Not Implemented"}
               }
)

@router.get("/")
async def getAuthors(db=Depends(get_db)):
    authors = db.query(Author).all()
    return {"authors": authors}


@router.get("/{id}")
async def getAuthor(id: int, db=Depends(get_db)):
    author = db.query(Author).filter(Author.author_id == id).first()
    return {"author": author}


@router.put("/{id}")
async def updateAuthor(id: int, author_data: AuthorSchema, db=Depends(get_db)):
    author = db.query(Author).filter(Author.author_id == id).first()
    if not author:
        raise HTTPException(status_code=404, detail="Author not found")

    author.first_name = author_data.first_name
    author.last_name = author_data.last_name
    author.birth_year = author_data.birth_year

    db.commit()
    db.refresh(author)
    return {"author": author}

@router.delete("/{id}")
async def deleteAuthor(id: int, db=Depends(get_db)):
    author = db.query(Author).filter(Author.author_id == id).first()
    if not author:
        raise HTTPException(status_code=404, detail="Author not found")
    db.delete(author)
    db.commit()
    return {"message": "Author deleted successfully"}   

@router.post("/")
async def createAuthor(author_data: AuthorSchema, db=Depends(get_db)):
    new_author = Author(
        first_name=author_data.first_name,
        last_name=author_data.last_name,
        birth_year=author_data.birth_year
    )
    db.add(new_author)
    db.commit()
    db.refresh(new_author)
    return {"author": new_author}

