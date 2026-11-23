import jwt
import datetime
from fastapi import Depends, HTTPException
from typing import Annotated
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from config import get_token_settings, TokenSettings


async def verify_token(credentials: Annotated[HTTPAuthorizationCredentials, Depends(HTTPBearer())], settings: TokenSettings = Depends(get_token_settings)):

    token = credentials.credentials
    try:
        payload =  jwt.decode(token, settings.Secret_Key, algorithms=["HS256"])

        user_name = str(payload.get("UserName"))
        email = str(payload.get("Email"))
        role = str(payload.get("Role"))

        if(user_name.lower() == settings.App_UserName.lower() and email.lower() == settings.Email.lower() and role.lower() ==  settings.Role.lower()):
            return
        else:
         raise HTTPException(status_code=401, detail="Invalid token")

    except jwt.PyJWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

    