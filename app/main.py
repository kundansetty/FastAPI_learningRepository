from fastapi import FastAPI, Response, status, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional
import random
import psycopg
from psycopg.rows import dict_row
import time
from dotenv import load_dotenv
import os

load_dotenv()

app = FastAPI()

class Post(BaseModel):
    title: str
    content: str

while True:
    try:
        conn = psycopg.connect(f"host={os.environ["DB_HOST"]} dbname={os.environ["DB_NAME"]} user={os.environ["DB_USER"]} password={os.environ["DB_PASSWORD"]}", row_factory=dict_row) # as conn:
        cur = conn.cursor() # as cur:
        break
    except Exception as error:
        print("Connection to database if faild with error: ", error)
        time.sleep(2)


# API

@app.get("/")
def home():
    return {"message": "Welcome to the social media"}

@app.get("/posts/{id}")
def get_post(id: int):
    cur.execute("""SELECT * FROM posts WHERE id = %s""", (str(id),))
    post = cur.fetchone()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"Post with the id: {id} was not found")

    return {"post": post}

@app.get("/posts")
def get_posts():
    cur.execute("""SELECT * FROM posts""")
    posts = cur.fetchall()
    print(posts)
    return {"posts": posts}

@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_post(payload: Post):
    cur.execute("""INSERT INTO posts (title, content) VALUES (%s, %s) RETURNING *""", (payload.title, payload.content))
    post = cur.fetchone()

    conn.commit()
    
    return {'data': post}

@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    cur.execute("""DELETE FROM posts WHERE id = %s RETURNING *""",(str(id),))
    post = cur.fetchone()
    
    conn.commit()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"There is no post with id: {id}")

    return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.put("/posts/{id}") 
def update_post(id: int, payload: Post):
    cur.execute("""UPDATE posts SET title = %s, content = %s WHERE id = %s RETURNING *""",(payload.title, payload.content, str(id)))
    post = cur.fetchone()

    conn.commit()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"The post with id: {id} does not exist")
    return {"post": post}