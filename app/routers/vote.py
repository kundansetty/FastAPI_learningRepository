from sqlmodel import select
from fastapi import status, HTTPException, APIRouter, Depends
from typing import Annotated
import database, models, schemas, oauth2
from sqlalchemy.exc import IntegrityError
from psycopg.errors import ForeignKeyViolation

router = APIRouter(
    prefix="/votes",
    tags = ["Votes"]
)

@router.post("/",status_code=status.HTTP_201_CREATED)
def vote(vote: schemas.Vote,
         session: database.sessionDep, 
         current_user: Annotated[schemas.UserResponse, Depends(oauth2.get_current_user)]):

    post_statement = select(models.Posts).where(models.Posts.id == vote.post_id, models.Posts.published == True)
    post = session.exec(post_statement).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post not found with id: {vote.post_id}")
    
    statement = select(models.Votes).where(
        models.Votes.post_id == vote.post_id).where(
            models.Votes.user_id == current_user.id)
    found_vote = session.exec(statement).first()
    if vote.dir == 1 and not found_vote:
        new_vote = models.Votes(user_id=current_user.id, post_id=vote.post_id)
        session.add(new_vote)
        session.commit()
        return {"message": "Successfully added a vote"}
    elif vote.dir == 0 and found_vote:
         session.delete(found_vote)
         session.commit()
         return {"message": "Successfully deleted the vote"}
    elif found_vote and vote.dir == 1:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Cannot vote a post twice")
    elif not found_vote and vote.dir == 0:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Vote does not exist")