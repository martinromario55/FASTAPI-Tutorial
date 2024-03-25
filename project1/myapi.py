from fastapi import FastAPI


app = FastAPI()

@app.get("/")
def idex():
    return {"message": "Hello World!"}