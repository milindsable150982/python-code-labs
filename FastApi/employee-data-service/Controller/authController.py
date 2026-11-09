from fastapi import APIRouter, Depends, HTTPException, status
from DataAccess.user import UserModel, User
from DataAccess.Database import SessionLocal, getDatabase
from sqlalchemy import func

router = APIRouter()

@router.post("/auth/", status_code=status.HTTP_201_CREATED)
async def CreateUser(user_data: UserModel, db: SessionLocal = Depends(getDatabase)):
    userData = User(**user_data.dict())
    db.add(userData)
    db.commit()
    db.refresh(userData)


@router.get("/auth")
async def GetUsers(db: SessionLocal = Depends(getDatabase)):
    return db.query(User).all()


@router.post("/authenticateuser")
async def AuthenticateUser(userName: str, password:str, db: SessionLocal = Depends(getDatabase)):
    userInfo  = db.query(User).filter(func.lower(User.UserName) == userName.lower(), func.lower(User.Password) == password.lower()).first()

    if(userInfo is None):
        return "Authemntication failed"
    else:
        return "Authemntication successful"
