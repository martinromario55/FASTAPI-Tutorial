from pydantic import BaseModel

# Post Schema
class Post(BaseModel):
    title: str
    content: str
    published: bool = True