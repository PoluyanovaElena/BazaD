import sqlite3

connection = sqlite3.connect("products.db")
cursor = connection.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS Products(
id INTEGER PRIMARY KEY,
title TEXT NOT NULL,
description TEXT NOT NULL,
price INTEGER NOT NULL
)
''')

cursor.execute("CREATE INDEX IF NOT EXISTS inx_description ON Products (description)")


def initiate_db():
    for i in range(4):
        cursor.execute("INSERT INTO Products (title, description, price) VALUES(?, ?, ?)",
                        (f"Продукт{i+1}", f"Описание{i+1}", 100 * (i + 1)))
    connection.commit()



def get_all_products():
    cursor.execute("SELECT * FROM Products")
    connection.commit()
    return cursor.fetchall()