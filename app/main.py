from fastapi import FastAPI, Response, status, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional
import random

app = FastAPI()

class Post(BaseModel):
    title: str
    content: str
    published: bool = True 
    rating: Optional[int] = None

my_posts = [
    {
        "id": 1,
        "title": "1st post",
        "content": "first content"
    },
    {
        "id": 2,
        "title": "2nd post",
        "content": "second content"
    }
]

# Funcitons
def find_index_post(id):
    for i, p in enumerate(my_posts):
        if p['id'] == id:
            return i
    return None

def find_post(id):
    for post in my_posts:
        if post['id'] == id:
            return post

    return None

# API

@app.get("/")
def home():
    return {"message": "Welcome to the social media"}

# @app.get("/posts/latest")
# def latest_post():
#     post = my_posts[-1]
#     return {"post": post}

@app.get("/posts/{id}")
def get_post(id: int):  # , response: Response):
    required_post = find_post(id)
    if required_post == None:
    #     response.status_code = status.HTTP_404_NOT_FOUND
    #     return {"Message": f"Post with the id: {id} was not found"}
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"Post with the id: {id} was not found")

    return {"post": required_post}

@app.get("/posts")
def get_posts():
    return {"posts": my_posts}

@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_post(payload: Post):
    payload = payload.model_dump()
    payload["id"] = random.randrange(0,10000000)
    my_posts.append(payload)
    return {'data': payload}

@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    index = find_index_post(id)
    if index == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"There is no post with id: {id}")
    else:
        del_post = my_posts.pop(index)
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.put("/posts/{id}")
def update_post(id: int, payload: Post):
    index = find_index_post(id)
    if index == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"The post with id: {id} does not exist")
    my_posts[index] = payload.model_dump()
    my_posts[index]['id'] = id
    return {"post": my_posts[index]}