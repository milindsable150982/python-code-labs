from fastapi import FastAPI, status, Request, Depends
from  DataAccess.config.database import Base, engine
import Controllers.memberController
import Controllers.bookController
import Controllers.authorController
import Controllers.borrowingController
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from config import get_token_settings
import jwt
from datetime import datetime, timedelta
from config import TokenSettings

from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from typing import Annotated
from fastapi import HTTPException

app = FastAPI()

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content=jsonable_encoder({"detail": exc.errors(), "body": exc.body}),
    )

@app.get("/getToken")
async def getToken(settings: TokenSettings = Depends(get_token_settings)):

    encode_claims =  {
        "UserName": settings.App_UserName,
        "Email": settings.Email,
        "Role": settings.Role,
        "exp": datetime.utcnow() + timedelta(minutes=30)
    }
    return jwt.encode(encode_claims, settings.Secret_Key, algorithm="HS256")

@app.get("/health", status_code=status.HTTP_200_OK)
async def health_check():
    return {"status": "healthy"}


app.include_router(Controllers.memberController.router)
app.include_router(Controllers.bookController.router)
app.include_router(Controllers.authorController.router)
app.include_router(Controllers.borrowingController.router)

Base.metadata.create_all(bind=engine)