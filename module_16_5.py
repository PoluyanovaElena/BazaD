from fastapi import FastAPI, status, Body, HTTPException, Request, Form
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from typing import List
from fastapi.templating import Jinja2Templates
app = FastAPI()
templates = Jinja2Templates(directory="templates")

users = []


class User(BaseModel):
    id: int
    username: str
    age: int


@app.get("/")
def get_all_users(request: Request) -> HTMLResponse:
    return templates.TemplateResponse("users.html", {"request": request, "users": users})


@app.get(path="/user/{user_id}")
async def get_users(request: Request, user_id: int) -> HTMLResponse:
    try:
        return templates.TemplateResponse("users.html", {"request": request, "user": users[user_id-1]})
    except IndexError:
        raise HTTPException(status_code=404, detail="User not found")


@app.post("/user/{username}/{age}")
async def post_user(username: str, age: int):
    if not users:
        new_id = 1
    else:
        max_id = 0
        for user in users:
            if user.id > max_id:
                max_id = user.id
        new_id = max_id + 1
    new_user = User(id=new_id, username=username, age=age)
    users.append(new_user)
    return new_user


@app.put("/user/{user_id}/{username}/{age}")
async def update_user(user_id: int, username: str, age: int):
    for user in users:
        if user.id == user_id:
            user = users[user_id-1]
            user.username = username
            user.age = age
            return f"The user {user_id} has been updated"
    raise HTTPException(status_code=404, detail="User was not found")


@app.delete("/user/{user_id}")
async def delete_user(user_id: int):
    for user in users:
        if user.id == user_id:
            del users[user_id-1]
            return f"User {user_id} has been deleted"
    raise HTTPException(status_code=404, detail="User was not found")