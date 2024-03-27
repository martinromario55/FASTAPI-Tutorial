from fastapi import FastAPI, Body, Response, status, HTTPException
from pydantic import BaseModel
from typing import Optional
from random import randrange

app = FastAPI()

# Post Schema
class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None
    
my_posts = [
    {
        "id": 1,
        "title": "My first post",
        "content": "This is my first post",
        "published": True,
        "rating": 10
    },
    {
        "id": 2,
        "title": "My second post",
        "content": "This is my second post",
        "published": True,
        "rating": 10
    }
]


@app.get("/")
def idex():
    return {"message": "Hello World!"}

@app.get('/posts')
def get_posts():
    return {"data": my_posts}

@app.post('/posts', status_code=status.HTTP_201_CREATED)
def create_posts(new_post: Post):
    post_dict = new_post.model_dump()
    post_dict["id"] = randrange(0,1000000)
    my_posts.append(post_dict)
    return {"data": post_dict}

@app.get('/posts/{id}')
def get_post(id: int, response: Response):
    for post in my_posts:
        if post["id"] == id:
            response.status_code = status.HTTP_200_OK
            return {"data": post}
    # response.status_code = status.HTTP_404_NOT_FOUND
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
    
@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    for post in my_posts:
        if post["id"] == id:
            my_posts.remove(post)
            return
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")

@app.put("/posts/{id}", status_code=status.HTTP_200_OK)
def update_post(id: int, new_post: Post):
    for post in my_posts:
        if post["id"] == id:
            post.update(new_post.model_dump())
            return {"data": post}
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")