from fastapi import FastAPI, Body

app = FastAPI()

@app.get("/")
def idex():
    return {"message": "Hello World!"}

@app.get('/posts')
def get_posts():
    return {"data": "These are your posts"}

@app.post('/createposts')
def create_posts(playload: dict = Body(...)):
    print(playload)
    return {"new_post": f"title {playload['title']} content: {playload['content']}"}