from fastapi import Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from typing import List, Optional

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
def get_posts(db: Session = Depends(get_db), current_user: int = Depends(get_current_user), limit: int = 10, skip: int = 0, search: Optional[str] = ""):
    # Get all posts
    # posts = db.query(models.Post).all()
    # print(posts)
    
    # Get all posts from current user
    # posts = db.query(models.Post).filter(models.Post.owner_id == current_user.id).all()
    
    # limit posts
    # posts = db.query(models.Post).limit(limit).all()
    
    # skip posts
    # posts = db.query(models.Post).offset(skip).limit(limit).all()
    
    # search posts
    posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).all()
    
    return posts

# Create Post
@router.post('/', status_code=status.HTTP_201_CREATED, response_model=Post)
def create_posts(post: PostCreate, db: Session = Depends(get_db), current_user: int = Depends(get_current_user)):
    
    # print(current_user.email)
    new_post = models.Post(owner_id=current_user.id, **post.model_dump())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    
    return new_post

# Get Post by Id
@router.get('/{id}', response_model=Post)
def get_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(get_current_user)):
    post = db.query(models.Post).filter(models.Post.id == id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
    return post

# Delete Post    
@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(get_current_user)):
    
    post_query = db.query(models.Post).filter(models.Post.id == id)
    
    post = post_query.first()
    
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
    
    # Check if current user owns the post
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You are not the owner of this post")
    
    post_query.delete(synchronize_session=False)
    db.commit()
    
    return Response(status_code=status.HTTP_204_NO_CONTENT)

# Update Post
@router.put("/{id}", response_model=Post)
def update_post(id: int, updated_post: PostCreate, db: Session = Depends(get_db), current_user: int = Depends(get_current_user)):
    
    post_query = db.query(models.Post).filter(models.Post.id == id)
    
    post = post_query.first()
    
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
    
    # Check if current user owns the post
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You are not the owner of this post")
    
    post_query.update(updated_post.model_dump(), synchronize_session=False)
    
    db.commit()
    
    return {"data": post_query.first()}
