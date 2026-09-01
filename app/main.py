from fastapi import FastAPI, Response, status, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.params import Body
from pydantic import BaseModel
import psycopg
from psycopg.rows import dict_row
import time
from dotenv import load_dotenv
import database
import models, schemas
from sqlmodel import select
import os
from typing import List

load_dotenv()

models.create_table(database.engine)

app = FastAPI()

# class Post(BaseModel):
    # title: str
    # content: str

'''
This is a connection setup using psycopg, since we shifted to SQLModel to connect to DB and execute query using ORM,
this piece of code is not required.
while True:
    try:
        conn = psycopg.connect(f"host={os.environ["DB_HOST"]} dbname={os.environ["DB_NAME"]} user={os.environ["DB_USER"]} password={os.environ["DB_PASSWORD"]}", row_factory=dict_row) # as conn:
        cur = conn.cursor() # as cur:
        break
    except Exception as error:
        print("Connection to database if faild with error: ", error)
        time.sleep(2)
'''


# API

@app.get("/")
def home():
    return {"message": "Welcome to the social media"}

@app.get("/posts/{id}", response_model=schemas.PostResponse)
def get_post(id: int, session: database.sessionDep):
    # cur.execute("""SELECT * FROM posts WHERE id = %s""", (str(id),))
    # post = cur.fetchone()
    post = session.get(models.Posts, id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"Post with the id: {id} was not found")

    return post

@app.get("/posts", response_model=List[schemas.PostResponse])
def get_posts(session: database.sessionDep):
    # cur.execute("""SELECT * FROM posts""")
    # posts = cur.fetchall()
    statement = select(models.Posts)
    posts = session.exec(statement).all()
    return posts

@app.post("/posts", status_code=status.HTTP_201_CREATED, response_model=schemas.PostResponse)
def create_post(payload: schemas.PostCreate, session: database.sessionDep):
    # cur.execute("""INSERT INTO posts (title, content) VALUES (%s, %s) RETURNING *""", (payload.title, payload.content))
    # post = cur.fetchone()

    # conn.commit()

    
    post = models.Posts(**payload.model_dump()) # '*' is used instead of using title = payload.title, content = payload.content, published = payload.published
    session.add(post)
    session.commit()
    session.refresh(post)
    return post

@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, session: database.sessionDep):
    # cur.execute("""DELETE FROM posts WHERE id = %s RETURNING *""",(str(id),))
    # post = cur.fetchone()
    
    # conn.commit()

    post = session.get(models.Posts, id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"There is no post with id: {id}")
    session.delete(post)
    session.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.put("/posts/{id}", response_model=schemas.PostResponse) 
def update_post(id: int, payload: schemas.PostCreate, session: database.sessionDep):
    # cur.execute("""UPDATE posts SET title = %s, content = %s WHERE id = %s RETURNING *""",(payload.title, payload.content, str(id)))
    # post = cur.fetchone()

    # conn.commit()

    post = session.get(models.Posts, id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"The post with id: {id} does not exist")

    update_post = payload.model_dump(exclude_unset=True)
    post.sqlmodel_update(update_post)
    session.add(post)
    session.commit()
    session.refresh(post)
    return post