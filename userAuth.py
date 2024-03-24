from fastapi import FastAPI, Depends, params

app = FastAPI()

# the dependency function:
def user_dep(name: str = params, password: str = params):
    return {"name": name, "valid": True}

# the pasth function / web endpoint
@app.get("/user")
def get_user(user: dict = Depends(user_dep)) -> dict:
    return user