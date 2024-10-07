import sqlite3

connection = sqlite3.connect("not_telegram.db")
cursor = connection.cursor()


def initiate_db():
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Products(
        id INTEGER PRIMARY KEY,
        title TEXT NOT NULL,
        description TEXT NOT NULL,
        price INTEGER NOT NULL
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Users(
        id INTEGER PRIMARY KEY,
        username TEXT NOT NULL,
        email TEXT NOT NULL,
        age INTEGER NOT NULL,
        balance INTEGER NOT NULL
    );
    ''')
    connection.commit()


def add_user(username, email, age):
    cursor.execute("INSERT INTO Users (username, email, age, balance) VALUES (?, ?, ?, 1000)",
                   (f"{username}", f"{email}", f"{age}"))
    connection.commit()


def get_all_products():
    cursor.execute("SELECT * FROM Products")
    connection.commit()
    return cursor.fetchall()


def is_included(username):
    cursor.execute("SELECT * FROM Users")
    users = cursor.fetchall()
    for user in users:
        if username == user[1]:
            return True
    return False
