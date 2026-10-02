from sqlmodel import select
from fastapi import status, HTTPException, APIRouter

import database, models, schemas, utils

router = APIRouter(
    prefix='/users',
    tags=['Users'   ]
)

@router.post('/', status_code=status.HTTP_201_CREATED, response_model=schemas.UserResponse)
def create_user(payload: schemas.UserCreate, session: database.sessionDep):

    check_user = session.exec(select(models.Users).where(models.Users.email == payload.email)).first()
    if check_user:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f'User Already Exists with User Name: {payload.email}')
    
    payload.password = utils.hash_password(payload.password) #hashing the password

    user = models.Users(**payload.model_dump())
    session.add(user)
    session.commit()
    session.refresh(user)

    return user

@router.get('/{id}', response_model=schemas.UserResponse)
def get_users(id: int, session: database.sessionDep):

    user = session.get(models.Users, id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'No user with the id:{id}')

    return user