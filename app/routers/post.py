from sqlmodel import select, or_, col, func
from fastapi import status, HTTPException, Response, APIRouter, Depends
from typing import List, Annotated, Optional

import database, models, schemas, oauth2

router = APIRouter(
    prefix='/posts', #common path URL for the post router
    tags=['Posts'] #Logically group the routers in swagger UI
)

@router.get("/{id}", response_model=schemas.PostVoteResponse)
def get_post(id: int, 
             session: database.sessionDep, 
             current_user: Annotated[schemas.UserResponse, Depends(oauth2.get_current_user)]): #get the current logged in user
    # cur.execute("""SELECT * FROM posts WHERE id = %s""", (str(id),))
    # post = cur.fetchone()
    # print(current_user)

    # post = session.get(models.Posts, id)

    statement = select(models.Posts, func.count(models.Votes.user_id).label("votes")).join(
        models.Votes,models.Posts.id == models.Votes.post_id, isouter=True).group_by(
            models.Posts.id).where(models.Posts.id == id).where(or_(models.Posts.published == True, models.Posts.user_id == current_user.id))

    post = session.exec(statement).all()
    
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"Post with the id: {id} was not found")

    results = list(map(lambda x : x._mapping, post))[0]

    return results

@router.get("/", response_model=List[schemas.PostVoteResponse])
def get_posts(session: database.sessionDep, current_user: Annotated[int, Depends(oauth2.get_current_user)],
              limit: int = 2, skip: int = 0, search: Optional[str] = ""):

    # cur.execute("""SELECT * FROM posts""")
    # posts = cur.fetchall()

    '''

    This "statement" was used when no joins were introduced to me and no voting system was enabled

    statement = select(models.Posts).where(
        or_(models.Posts.published == True, models.Posts.user_id == current_user.id)).where(
            col(models.Posts.title).contains(search)).order_by(
            models.Posts.published, models.Posts.created_at).limit(limit).offset(skip)
    '''

    statement = select(models.Posts, func.count(models.Votes.user_id).label("votes")).join(
        models.Votes,models.Posts.id == models.Votes.post_id, isouter=True).group_by(
            models.Posts.id).where(
        or_(models.Posts.published == True, models.Posts.user_id == current_user.id)).where(
            col(models.Posts.title).contains(search)).order_by(
            models.Posts.published, models.Posts.created_at).limit(limit).offset(skip)
    posts = session.exec(statement).all()

    '''
        When select statement has two arguments it returns a Row object instead of dict. So, when we return a row object without
        converting it into list, it raise errors.
    '''
    results = list(map(lambda x : x._mapping, posts))

    print(results)

    return results

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.PostResponse)
def create_post(payload: schemas.PostCreate, 
                session: database.sessionDep, 
                current_user: Annotated[int, Depends(oauth2.get_current_user)]):
    # cur.execute("""INSERT INTO posts (title, content) VALUES (%s, %s) RETURNING *""", (payload.title, payload.content))
    # post = cur.fetchone()

    # conn.commit()

    post = models.Posts(user_id = current_user.id, **payload.model_dump()) # '*' is used instead of using title = payload.title, content = payload.content, published = payload.published
    session.add(post)
    session.commit()
    session.refresh(post)
    return post

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, session: database.sessionDep, 
                current_user: Annotated[int, Depends(oauth2.get_current_user)]):
    # cur.execute("""DELETE FROM posts WHERE id = %s RETURNING *""",(str(id),))
    # post = cur.fetchone()
    
    # conn.commit()

    post = session.get(models.Posts, id)

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"There is no post with id: {id}")

    if post.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform the requested action")
    
    session.delete(post)
    session.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.put("/{id}", response_model=schemas.PostResponse) 
def update_post(id: int, 
                payload: schemas.PostCreate, 
                session: database.sessionDep,
                current_user: Annotated[int, Depends(oauth2.get_current_user)]):
    # cur.execute("""UPDATE posts SET title = %s, content = %s WHERE id = %s RETURNING *""",(payload.title, payload.content, str(id)))
    # post = cur.fetchone()

    # conn.commit()

    post = session.get(models.Posts, id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"The post with id: {id} does not exist")

    if post.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform the requested action")

    update_post = payload.model_dump(exclude_unset=True)
    post.sqlmodel_update(update_post)
    session.add(post)
    session.commit()
    session.refresh(post)
    return post