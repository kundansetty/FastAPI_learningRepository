import jwt, os
from jwt.exceptions import InvalidTokenError, ExpiredSignatureError
from fastapi import Depends, HTTPException, status 
from fastapi.security import OAuth2PasswordBearer
from typing import Annotated
from datetime import datetime, timedelta, UTC
import schemas, database, models
from dotenv import load_dotenv
from sqlmodel import select

#SECRET_KEY
#Algorithm
#expiration time

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='login')

load_dotenv()

def create_access_token(data: dict):
    to_encode = data.copy()

    exipires = datetime.now(UTC) + timedelta(minutes=int(os.environ['ACCESS_TOKEN_EXPIRE_MINUTES']))
    to_encode.update({"exp": exipires})
    encoded_jwt = jwt.encode(to_encode, os.environ['SECRET_KEY'], os.environ['ALGORITHM'])
    return encoded_jwt

def verfiy_access_token(token: str, credentials_exception):
    try: 
        payload = jwt.decode(token, os.environ['SECRET_KEY'], algorithms=[os.environ['ALGORITHM']])
        id = payload.get("user_id")
        if id is None:
            raise credentials_exception
        token_data = schemas.TokenData(id = id)

    except ExpiredSignatureError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Token has expired. Please log in again.",
                            headers={"WWW-Authenticate": "Bearer"})
    
    except InvalidTokenError:
        raise credentials_exception

    return token_data

def get_current_user(token: Annotated[str, Depends(oauth2_scheme)], session: database.sessionDep):
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, 
                                          detail='Could not Validate Credentials',
                                          headers={"WWW-Authenticate": "Bearer"})
    token_data = verfiy_access_token(token=token, credentials_exception=credentials_exception)
    user: schemas.UserResponse = session.exec(select(models.Users).where(models.Users.id == token_data.id)).first()
    return user