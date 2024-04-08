from fastapi import FastAPI

from . import models
from .database import engine, get_db
from .utils import hash
from .routers import post, user, auth
from .config import settings


# print(settings.database_username)


# Create a database connection
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# routers
app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)

@app.get("/")
def index():
    return {"message": "Hello World!"}