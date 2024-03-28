from fastapi import FastAPI, Body, Response, status, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List

from .schemas import PostCreate, Post, UserCreate, UserOut
from . import models
from .database import engine, get_db


# Create a database connection
models.Base.metadata.create_all(bind=engine)

app = FastAPI()


@app.get("/")
def index():
    return {"message": "Hello World!"}

# Get All Posts
@app.get('/posts', response_model=List[Post])
def get_posts(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()
    # print(posts)
    return posts

# Create Post
@app.post('/posts', status_code=status.HTTP_201_CREATED, response_model=Post)
def create_posts(post: PostCreate, db: Session = Depends(get_db)):
    
    new_post = models.Post(**post.model_dump())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    
    return new_post

# Get Post by Id
@app.get('/posts/{id}', response_model=Post)
def get_post(id: int, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
    return post

# Delete Post    
@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db)):
    
    post = db.query(models.Post).filter(models.Post.id == id)
    
    if post.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
    
    post.delete(synchronize_session=False)
    db.commit()
    
    return Response(status_code=status.HTTP_204_NO_CONTENT)

# Update Post
@app.put("/posts/{id}", response_model=Post)
def update_post(id: int, updated_post: PostCreate, db: Session = Depends(get_db)):
    
    post_query = db.query(models.Post).filter(models.Post.id == id)
    
    post = post_query.first()
    
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
    
    post_query.update(updated_post.model_dump(), synchronize_session=False)
    
    db.commit()
    
    return {"data": post_query.first()}


# Create new User
@app.post('/users', status_code=status.HTTP_201_CREATED, response_model=UserOut)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    new_user = models.User(**user.model_dump())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    return new_user