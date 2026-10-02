from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from typing import Annotated
import database, schemas, models, utils, oauth2
from sqlmodel import select


router = APIRouter(
    tags = ['authentication']
)


@router.post('/login', status_code=status.HTTP_200_OK, response_model=schemas.Token)
async def login(payload: Annotated[OAuth2PasswordRequestForm, Depends()], session: database.sessionDep):
    #OAuth2PassweordRequestForm returns a username and password
    statement = select(models.Users).where(models.Users.email == payload.username)
    user = session.exec(statement).first()

    if not user or not utils.verify_password(payload.password, user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Incorrect username or password')

    access_token = oauth2.create_access_token(data = {"user_id": user.id})
    
    return {'access_token': access_token,
            "token_type": "bearer"}