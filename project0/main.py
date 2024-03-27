from fastapi import FastAPI, Body, Response, status, HTTPException
from pydantic import BaseModel
from typing import Optional
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time

app = FastAPI()

# Post Schema
class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None
    
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

@app.get('/posts')
def get_posts():
    cursor.execute("""SELECT * FROM posts""")
    posts = cursor.fetchall()
    # print(posts)
    return {"data": posts}

@app.post('/posts', status_code=status.HTTP_201_CREATED)
def create_posts(post: Post):
    cursor.execute("""INSERT INTO posts (title, content, published) VALUES(%s, %s, %s) RETURNING * """, 
                   (post.title, post.content, post.published))
    
    new_post = cursor.fetchone()
    conn.commit()
    return {"new_post": new_post}

@app.get('/posts/{id}')
def get_post(id: int):
    cursor.execute("""SELECT * FROM posts WHERE id = %s""", (str(id),))
    post = cursor.fetchone()
    # print(post)
    if not post:
        # response.status_code = status.HTTP_404_NOT_FOUND
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
    return {"post_detail": post}
    
@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    cursor.execute("""DELETE FROM posts WHERE id = %s RETURNING *""", (str(id),))
    deleted_post = cursor.fetchone()
    
    if deleted_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
    conn.commit()

@app.put("/posts/{id}", status_code=status.HTTP_200_OK)
def update_post(id: int, post: Post):
    cursor.execute("""UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *""", 
                   (post.title, post.content, post.published, str(id)))
    updated_post = cursor.fetchone()
    
    if updated_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
    
    conn.commit()
    
    return {"data": updated_post}