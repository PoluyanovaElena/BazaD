from fastapi import FastAPI, status, Body, HTTPException
from pydantic import BaseModel
from typing import List
app = FastAPI()
users = []


class User(BaseModel):
    id: int
    username: str
    age: int


@app.get("/users")
async def get_users() -> List[User]:
    return users


@app.post("/user/{username}/{age}")
async def post_user(username: str, age: int):
    user_id = len(users) + 1
    new_user = User(id=user_id, username=username, age=age)
    users.append(new_user)
    return {f"User {user_id} is registered"}


@app.put("/user/{user_id}/{username}/{age}")
async def update_user(user_id: int, username: str, age: int):
    for user in users:
        if user.id == user_id:
            user = users[user_id-1]
            user.username = username
            user.age = age
            return user
    raise HTTPException(status_code=404, detail="User was not found")

# @app.put("/user/{user_id}/{username}/{age}")
# async def update_user(user_id: int, username: str, age: int):
#     try:
#         users[user_id] = f"Имя: {username}, возраст: {age}"
#         return f"The user {user_id} has been updated"
#     except IndexError:
#         raise HTTPException(status_code=404, detail="User was not found")


@app.delete("/user/{user_id}")
async def delete_user(user_id: int):
    try:
        del users[user_id]
        return f"User {user_id} has been deleted"
    except IndexError:
        raise HTTPException(status_code=404, detail="User was not found")

