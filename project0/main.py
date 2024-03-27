from fastapi import FastAPI, Body
from pydantic import BaseModel
from typing import Optional

app = FastAPI()

# Post Schema
class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None


@app.get("/")
def idex():
    return {"message": "Hello World!"}

@app.get('/posts')
def get_posts():
    return {"data": "These are your posts"}

@app.post('/createposts')
def create_posts(new_post: Post):
    # print(new_post)
    print(new_post.model_dump())
    return {"data": "new_post"}