from fastapi import FastAPI

app = FastAPI()


@app.get("/")
async def main_page():
    return {"message": "Главная страница"}


@app.get("/user/admin")
async def main_admin():
    return {"message": "Вы вошли как администратор"}


@app.get("/user/{user_id}")
async def main_user(user_id: int):
    return {f"Вы вошли как пользователь № {user_id}"}


@app.get("/user/{username}/{age}")
async def main_user_info(username: str, age: int):
    return {f"Информация о пользователе. Имя: {username}, Возраст: {age}"}

