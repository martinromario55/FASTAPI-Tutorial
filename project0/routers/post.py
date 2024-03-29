from fastapi import Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from typing import List

from ..schemas import PostCreate, Post
from .. import models
from ..database import get_db
from ..oauth2 import get_current_user

router = APIRouter(
    prefix='/posts',
    tags=['Posts']
)

# Get All Posts
@router.get('/', response_model=List[Post])
def get_posts(db: Session = Depends(get_db), user_id: int = Depends(get_current_user)):
    posts = db.query(models.Post).all()
    # print(posts)
    return posts

# Create Post
@router.post('/', status_code=status.HTTP_201_CREATED, response_model=Post)
def create_posts(post: PostCreate, db: Session = Depends(get_db), user_id: int = Depends(get_current_user)):
    
    print(user_id)
    new_post = models.Post(**post.model_dump())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    
    return new_post

# Get Post by Id
@router.get('/{id}', response_model=Post)
def get_post(id: int, db: Session = Depends(get_db), user_id: int = Depends(get_current_user)):
    post = db.query(models.Post).filter(models.Post.id == id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
    return post

# Delete Post    
@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db), user_id: int = Depends(get_current_user)):
    
    post = db.query(models.Post).filter(models.Post.id == id)
    
    if post.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
    
    post.delete(synchronize_session=False)
    db.commit()
    
    return Response(status_code=status.HTTP_204_NO_CONTENT)

# Update Post
@router.put("/{id}", response_model=Post)
def update_post(id: int, updated_post: PostCreate, db: Session = Depends(get_db), user_id: int = Depends(get_current_user)):
    
    post_query = db.query(models.Post).filter(models.Post.id == id)
    
    post = post_query.first()
    
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
    
    post_query.update(updated_post.model_dump(), synchronize_session=False)
    
    db.commit()
    
    return {"data": post_query.first()}
