from fastapi import APIRouter, Depends, HTTPException, status
from DataAccess.user import UserModel, User
from DataAccess.Database import SessionLocal, getDatabase
from typing import Annotated
from sqlalchemy import func
import jwt
from datetime import datetime, timedelta
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

router = APIRouter()

Secrete_Key = "0563ddd2-44bb-451e-b133-de344b61e478"  # Replace with your actual secret key
Algorithm = "HS256"  # Replace with your desired algorithm 

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

    token = GenerateToken(userInfo.UserName, userInfo.id)
    if(userInfo is None):
        return "Authemntication failed"
    else:
        return {"token": token}


def GenerateToken(userName: str, userId: int):
    payload = {"sub": userName, "user_id": userId}
    dateTime = datetime.utcnow() + timedelta(minutes=30)  # Token expiration time
    payload.update({"exp": dateTime})
    token = jwt.encode(payload, Secrete_Key, algorithm=Algorithm)
    return token


def FetchToken(credentials: Annotated[HTTPAuthorizationCredentials, Depends(HTTPBearer())], db: SessionLocal = Depends(getDatabase)):
    token = credentials.credentials

    try:
        payload = jwt.decode(token, Secrete_Key, algorithms=["HS256"])
    except jwt.PyJWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

    username = payload.get("sub")
    userId = payload.get("user_id")
    userInfo  = db.query(User).filter(func.lower(User.UserName) == username.lower(), User.id == userId).first()

    if(userInfo is None):
        raise HTTPException(status_code=401, detail="Invalid token")
