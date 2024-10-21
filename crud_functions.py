# -*- coding: utf-8 -*-
# crud_functions.py
import sqlite3

database_name = "food_warehouse.db"
table_name = "Products"


def initiate_db() -> None:
    try:
        connection = sqlite3.connect(database_name)  # Если такого файла не существует, он будет создан автоматически
        cursor = connection.cursor()
    except sqlite3.Error as error1:
        print(f"Ошибка. {error1}")
    else:
        cursor.execute(f'''
            CREATE TABLE IF NOT EXISTS {table_name}(
            id INTEGER PRIMARY KEY,
            title TEXT NOT NULL,
            description TEXT, 
            price INTEGER NOT NULL
            );
            ''')
        connection.commit()
        cursor.close()
    finally:
        if connection:
            connection.close()


def get_all_products() -> list:
    connection = sqlite3.connect(database_name)
    cursor = connection.cursor()

    products_list_to_return = []  # Список на выход
    try:
        # Получить все записи из таблицы "Products"
        cursor.execute(f'''
           SELECT * FROM {table_name};
           ''')
        products = cursor.fetchall()
    except sqlite3.Error as error2:
        print(f"Ошибка. {error2}")
        return products_list_to_return

    for product in products:
        # id, title, description, price
        product_string = f"Название: {product[1]}| Описание: {product[2]}| Цена: {product[3]} "
        products_list_to_return.append(product_string)  # Список на выход
    # Это конец
    cursor.close()
    connection.close()
    return products_list_to_return


def add_4_rows_to_products() -> list:
    connection = sqlite3.connect(database_name)
    cursor = connection.cursor()
    # Строки, которые будут вставлены в таблицу "Products"
    # id - автоматически, title, description, price
    rows_to_be_inserted = []
    for i in range(4):
        row_i = (f"Продукт{i + 1}", f"описание{i + 1}", 100 * (i + 1))
        rows_to_be_inserted.append(row_i)
    # Try to insert
    try:
        sql1 = "INSERT INTO Products (title, description, price) VALUES (?, ?, ?)"
        cursor.executemany(sql1, rows_to_be_inserted)
        connection.commit()
    except sqlite3.Error as error3:
        print(f"Ошибка. {error3}")
    finally:
        cursor.close()
        connection.close()
    return rows_to_be_inserted

"""
print("----- Создаём таблицу 'Products' ")
initiate_db()
print("----- Добавим 4 записи в таблицу 'Products'")
print(add_4_rows_to_products())
print("----- Выводим все записи из таблицы 'Products'")
print(get_all_products())
print("------- The End -------")
"""
