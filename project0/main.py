from fastapi import FastAPI, Body, Response, status, HTTPException, Depends
from .schemas import Post
import psycopg2
from psycopg2.extras import RealDictCursor
from sqlalchemy.orm import Session
from . import models
from .database import engine, get_db


# Create a database connection
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

    
# Postgres Init
try:
    conn = psycopg2.connect(
        host="localhost",
        user="postgres",
        password="202022141057",
        port="5432",
        database="fastapidb"
    )
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    print('Database connection was successfull!')
    
    

except Exception as Error:
    print("Connection to database failed")
    print('Error:', Error)
    
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
def index():
    return {"message": "Hello World!"}

@app.get('/sqlalchemy')
def test_posts(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()
    return {"data": posts}

# Get All Posts
@app.get('/posts')
def get_posts(db: Session = Depends(get_db)):
    # cursor.execute("""SELECT * FROM posts""")
    # posts = cursor.fetchall()
    posts = db.query(models.Post).all()
    # print(posts)
    return {"data": posts}

# Create Post
@app.post('/posts', status_code=status.HTTP_201_CREATED)
def create_posts(post: Post, db: Session = Depends(get_db)):
    # cursor.execute("""INSERT INTO posts (title, content, published) VALUES(%s, %s, %s) RETURNING * """, 
    #                (post.title, post.content, post.published))
    
    # new_post = cursor.fetchone()
    # conn.commit()
    
    new_post = models.Post(**post.model_dump())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    
    return {"new_post": new_post}

# Get Post by Id
@app.get('/posts/{id}')
def get_post(id: int, db: Session = Depends(get_db)):
    # cursor.execute("""SELECT * FROM posts WHERE id = %s""", (str(id),))
    # post = cursor.fetchone()
    # # print(post)
    post = db.query(models.Post).filter(models.Post.id == id).first()
    if not post:
        # response.status_code = status.HTTP_404_NOT_FOUND
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
    return {"post_detail": post}

# Delete Post    
@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db)):
    # cursor.execute("""DELETE FROM posts WHERE id = %s RETURNING *""", (str(id),))
    # deleted_post = cursor.fetchone()
    
    post = db.query(models.Post).filter(models.Post.id == id)
    
    if post.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
    
    post.delete(synchronize_session=False)
    db.commit()
    
    return Response(status_code=status.HTTP_204_NO_CONTENT)

# Update Post
@app.put("/posts/{id}", status_code=status.HTTP_200_OK)
def update_post(id: int, updated_post: Post, db: Session = Depends(get_db)):
    # cursor.execute("""UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *""", 
    #                (post.title, post.content, post.published, str(id)))
    # updated_post = cursor.fetchone()
    
    post_query = db.query(models.Post).filter(models.Post.id == id)
    
    post = post_query.first()
    
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
    
    post_query.update(updated_post.model_dump(), synchronize_session=False)
    
    db.commit()
    
    return {"data": post_query.first()}