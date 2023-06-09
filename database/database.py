"""
data base 
"""
import datetime
# import pandas as pd
import sqlite3

import xlsxwriter as xlsxwriter

# import xlsxwriter

from config import DATABASE_NAME
from datetime import datetime

# create database
def create_database():
    """
    :return:
    """
    conn = sqlite3.connect(DATABASE_NAME)

    conn.execute('''CREATE TABLE IF NOT EXISTS Adminlar
                    (ID INTEGER PRIMARY KEY AUTOINCREMENT,
                     Ism TEXT NOT NULL,
                     Familiya TEXT NOT NULL,
                     Telefon TEXT NOT NULL,
                     Aloqa TEXT NOT NULL,
                     Tg_id TEXT NOT NULL);''')
    conn.execute('''CREATE TABLE IF NOT EXISTS SupAdminlar
                    (ID INTEGER PRIMARY KEY AUTOINCREMENT,
                    Ism TEXT NOT NULL,
                    Familiya TEXT NOT NULL,
                    Telefon TEXT NOT NULL,
                    Aloqa TEXT NOT NULL,
                    Tg_id TEXT NOT NULL);''')
    conn.execute('''CREATE TABLE IF NOT EXISTS users 
                     (id INTEGER PRIMARY KEY AUTOINCREMENT,
                      name TEXT NOT NULL,
                      phone_number TEXT,
                      viloyat TEXT NOT NULL,
                      address TEXT,
                      aloqa TEXT,
                      tuman TEXT,
                      Tg_id TEXT NOT NULL)''')
    conn.execute('''CREATE TABLE IF NOT EXISTS products 
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  name TEXT NOT NULL,
                  about TEXT,
                  price TEXT NOT NULL,
                  foto TEXT NOT NULL,
                  show TEXT NOT NULL,
                  category TEXT NOT NULL)''')
    conn.execute('''CREATE TABLE IF NOT EXISTS orders 
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  product INTEGER NOT NULL,
                  number_of_orders TEXT,
                  cament TEXT,
                  deta TEXT,
                  user_tg_id INTEGER NOT NULL,
                  user_id INTEGER NOT NULL)''')
    conn.execute('''CREATE TABLE IF NOT EXISTS categories 
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  name TEXT NOT NULL)''')
    conn.commit()

    conn.close()


def add_admin(ism: str, familiya: str, telefon: str, aloqa: str, tg_id: str) -> bool:
    """
    :param ism:
    :param familiya:
    :param telefon:
    :param aloqa:
    :param tg_id:
    :return:
    """
    try:
        conn = sqlite3.connect(DATABASE_NAME)
        conn.execute("INSERT INTO Adminlar (Ism, Familiya, Telefon, Aloqa, Tg_id) VALUES (?, ?, ?, ?, ?)",
                     (ism, familiya, telefon, aloqa, tg_id))
        conn.commit()
        conn.close()
        print(f"Info: database/add_admin -> True")
        return True
    except Exception as e:
        print(f"Error: database/add_admin -> {e}")
        return False


def is_admin(tg_id: str) -> bool:
    """
    :param tg_id:
    :return:
    """
    try:
        conn = sqlite3.connect(DATABASE_NAME)
        result = conn.execute("SELECT COUNT(*) FROM Adminlar WHERE Tg_id=?", (tg_id,)).fetchone()
        conn.close()
        print(f"Info: database/is_admin -> {result[0] > 0}")
        return result[0] > 0
    except Exception as e:
        print(f"Error: database/is_admin -> {e}")
        return False


def is_supadmin(tg_id: str) -> bool:
    """
    :param tg_id:
    :return:
    """
    try:
        conn = sqlite3.connect(DATABASE_NAME)
        result = conn.execute("SELECT COUNT(*) FROM SupAdminlar WHERE Tg_id=?", (tg_id,)).fetchone()
        conn.close()
        print(f"Info: database/is_supadmin -> {result[0] > 0}")
        return result[0] > 0
    except Exception as e:
        print(f"Error: database/is_supadmin -> {e}")
        return False


def is_user(tg_id: str) -> bool:
    """
    :param tg_id:
    :return:
    """
    try:
        conn = sqlite3.connect(DATABASE_NAME)
        result = conn.execute("SELECT COUNT(*) FROM users WHERE Tg_id=?", (tg_id,)).fetchone()
        conn.close()
        print(f"Info: database/is_user -> True")
        return result[0] > 0
    except Exception as e:
        print(f"Error: database/is_user -> {e}")
        return False


def categories() -> (bool, list):
    """
    :return:
    """
    try:
        conn = sqlite3.connect(DATABASE_NAME)
        result = conn.execute("SELECT * FROM categories").fetchall()
        conn.close()
        print(f"Info: database/categories -> True")
        return [row[1] for row in result]
    except Exception as e:
        print(f"Error: database/categories -> {e}")
        return False


def add_category(name: str) -> bool:
    """
    :param name:
    :return:
    """
    try:
        conn = sqlite3.connect(DATABASE_NAME)
        conn.execute("INSERT INTO categories (name) VALUES (?)", (name,))
        conn.commit()
        conn.close()
        print(f"Info: database/add_categories -> {True}")
        return True
    except Exception as e:
        print(f"Error: database/add_categories -> {e}")
        return False


def add_product_(name: str, category: str, about: str, price: str, photo: str, show="True") -> bool:
    """
    :param show:
    :param name: str, product name
    :param category: str, category name from categories table
    :param about: str, product description
    :param price: float, product price
    :param photo: str, photo url or file path of product
    :return: bool, True if product is added successfully, otherwise False
    """
    try:
        conn = sqlite3.connect(DATABASE_NAME)
        conn.execute(
            "INSERT INTO products (name, category, about, price, foto, show) VALUES (?, ?, ?, ?, ?, ?)",
            (name, category, about, price, photo, show)
        )
        conn.commit()
        conn.close()
        print("Info: database/add_product -> True")
        return True
    except Exception as e:
        print(f"Error: database/add_product -> {e}")
        return False


def products(category: str) -> (bool, list):
    """
    :param category:
    :return:
    """
    try:
        conn = sqlite3.connect(DATABASE_NAME)
        result = conn.execute("SELECT name FROM products WHERE category=? AND show=?", (category, "True")).fetchall()
        conn.close()
        print(f"Info: database/products -> True")
        return [row[0] for row in result]
    except Exception as e:
        print(f"Info: database/products -> {e}")
        return False



def product(category: str, product: str) -> (bool, list):
    try:
        conn = sqlite3.connect(DATABASE_NAME)
        result = conn.execute("SELECT name, about, price, foto, id FROM products WHERE category=? AND name=?",
                              (category,
                                                                                           product)).fetchone()
        conn.close()
        if result:
            print(f"Info: database/product -> True")
            return list(result)
        else:
            print(f"Info: database/product -> No such product exists.")
            return []
    except Exception as e:
        print(f"Info: database/product -> {e}")
        return False


def remove_category(category_: str) -> bool:
    """
    Removes the category with the given name from the database.
    :param category_: name of the category to be removed
    :return: True if the category was removed successfully, False otherwise
    """
    try:
        conn = sqlite3.connect(DATABASE_NAME)
        conn.execute("DELETE FROM categories WHERE name=?", (category_,))
        conn.commit()
        conn.close()
        print("Info: database/remove_category -> True")
        return True
    except Exception as e:
        print(f"Info: database/remove_category -> {e}")
        return False

def remove_product(product_name: str, category_name: str) -> bool:
    """
    Remove a product from the database based on its name and category name
    :param product_name: name of the product
    :param category_name: name of the category
    :return: True if the product is removed successfully, False otherwise
    """
    try:
        conn = sqlite3.connect(DATABASE_NAME)
        conn.execute("UPDATE products SET show=False WHERE name=? AND category=?", (product_name, category_name))
        conn.commit()
        conn.close()
        print(f"Info: database/remove_product -> True")
        return True
    except Exception as e:
        print(f"Info: database/remove_product -> {e}")
        return False


def get_user_by_tg_ids(tg_id: str) -> (bool, dict):
    try:
        conn = sqlite3.connect(DATABASE_NAME)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE Tg_id = ?", (tg_id,))
        results = cursor.fetchall()
        results = results[-1]
        conn.close()
        if results:
            result = results
        #     rresult = {}
        #     for result in results:
            user = {
                "id": result[0],
                "name": result[1],
                "phone_number": result[2],
                "aloqa": result[5],
                "viloyat": result[3],
                "tuman": result[6],
                "address": result[4],
                "tg_id": result[7]
            }
                # rresult[result[1]] = user
            print("Info: database/get_user_by_tg_ids -> True")
            return user
        else:
            print("Info: database/get_user_by_tg_ids -> User not found")
            return False
    except Exception as e:
        print(f"Info: database/get_user_by_tg_ids -> {e}")
        return False


def get_user_by_id_ids(_id: str) -> (bool, dict):
    try:
        conn = sqlite3.connect(DATABASE_NAME)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE id = ?", (_id,))
        results = cursor.fetchone()
        # results = results[-1]
        conn.close()
        if results:
            result = results
        #     rresult = {}
        #     for result in results:
            user = {
                "id": result[0],
                "name": result[1],
                "phone_number": result[2],
                "aloqa": result[5],
                "viloyat": result[3],
                "tuman": result[6],
                "address": result[4],
                "tg_id": result[7]
            }
                # rresult[result[1]] = user
            print("Info: database/get_user_by_id_ids -> True")
            return user
        else:
            print("Info: database/get_user_by_id_ids -> User not found")
            return False
    except Exception as e:
        print(f"Info: database/get_user_by_id_ids -> {e}")
        return False


def get_product_id(name: str, category: str) -> int:
    """
    :param name: Mahsulot nomi
    :param category: Mahsulot kategoriyasi
    :return: Mahsulot ID si
    """
    try:
        conn = sqlite3.connect(DATABASE_NAME)
        result = conn.execute("SELECT id FROM products WHERE name=? AND category=?", (name, category)).fetchone()
        conn.close()
        if result:
            print(f"Info: database/get_product_id -> True")
            return result[0]
        else:
            print(f"Error: database/get_product_id -> Mahsulot topilmadi.")
            return False
    except Exception as e:
        print(f"Error: database/get_product_id -> {e}")
        return False


def get_product_all_data_by_id(id_: int) -> (list, bool):
    """
    :param id_: Mahsulot idsi
    :return: Mahsulot malumotlari
    """
    try:
        conn = sqlite3.connect(DATABASE_NAME)
        result = conn.execute("SELECT name, about, price, foto, id FROM products WHERE id=?", (id_,)).fetchone()
        conn.close()
        if result:
            print(f"Info: database/get_product_all_data_by_id -> True")
            return result
        else:
            print(f"Error: database/get_product_all_data_by_id -> Mahsulot topilmadi.")
            return False
    except Exception as e:
        print(f"Error: database/get_product_id -> {e}")
        return False


def add_order(product: str, number_of_orders: int, user_id: str, user_tg_id: str, cament: str,) -> bool:
    """
    Adds a new order to the database.

    :param cament: cament order
    :param user_id: is user id
    :param product: ID of the product being ordered
    :param number_of_orders: number of products being ordered
    :param user_tg_id: ID of the user placing the order
    :return: True if the order is added successfully, False otherwise
    """
    try:
        conn = sqlite3.connect(DATABASE_NAME)
        conn.execute("INSERT INTO orders (product, number_of_orders, user_id, cament, user_tg_id, deta) VALUES (?, ?, "
                     "?, "
                     "?, "
                     "?, "
                     "?)",
                     (product, number_of_orders, user_id, cament, user_tg_id, str(datetime.now())))
        conn.commit()
        conn.close()
        print(f"Info: database/add_order -> True")
        return True
    except Exception as e:
        print(f"Error: database/add_order -> {e}")
        return False


def add_new_user(name: str, phone_number: str, aloqa: str, viloyat: str, tuman: str, address: str, tg_id: str) -> bool:
    """
    Add new user to the database.
    :param name: str, user name
    :param phone_number: str, user phone number
    :param aloqa: str, user contact information
    :param viloyat: str, user region
    :param tuman: str, user district
    :param address: str, user address
    :param tg_id: str, user telegram ID
    :return: bool, True if user added successfully, otherwise False
    """
    try:
        conn = sqlite3.connect(DATABASE_NAME)
        conn.execute("INSERT INTO users (name, phone_number, aloqa, viloyat, tuman, address, tg_id) VALUES (?, ?, ?, ?, ?, ?, ?)",
                     (name, phone_number, aloqa, viloyat, tuman, address, tg_id))
        conn.commit()
        conn.close()
        print(f"Info: database/add_new_user -> True")
        return True
    except Exception as e:
        print(f"Error: database/add_new_user -> {e}")
        return False


def change_user_data(user_id: int, name: str = None, phone_number: str = None, aloqa: str = None, viloyat: str = None,
                     tuman: str = None,
                     address: str = None, tg_id: str = None) -> bool:
    """
    Change user data.
    :param user_id: int, user ID in the database
    :param name: str, username
    :param phone_number: str, user phone number
    :param aloqa: str, user contact information
    :param viloyat: str, user region
    :param tuman: str, user district
    :param address: str, user address
    :param tg_id: str, user telegram ID
    :return: bool, True if user data changed successfully, otherwise False
    """
    try:
        conn = sqlite3.connect(DATABASE_NAME)
        update_columns = []
        update_values = []
        if name:
            update_columns.append("name = ?")
            update_values.append(name)
        if phone_number:
            update_columns.append("phone_number = ?")
            update_values.append(phone_number)
        if aloqa:
            update_columns.append("aloqa = ?")
            update_values.append(aloqa)
        if viloyat:
            update_columns.append("viloyat = ?")
            update_values.append(viloyat)
        if tuman:
            update_columns.append("tuman = ?")
            update_values.append(tuman)
        if address:
            update_columns.append("address = ?")
            update_values.append(address)
        if tg_id:
            update_columns.append("tg_id = ?")
            update_values.append(tg_id)
        if not update_columns:
            return False
        update_columns_str = ", ".join(update_columns)
        query = f"UPDATE users SET {update_columns_str} WHERE id = ?"
        update_values.append(user_id)
        conn.execute(query, tuple(update_values))
        conn.commit()
        conn.close()
        print(f"Info: database/change_user_data -> True")
        return True
    except Exception as e:
        print(f"Error: database/change_user_data -> {e}")
        return False


def get_orders_by_user_tg_id(tg_id: str) -> list:
    """
    Returns a list of orders made by a user with the given tg_id
    :param tg_id:
    :return: list of orders
    """
    try:
        conn = sqlite3.connect(DATABASE_NAME)
        orders = conn.execute("SELECT * FROM orders WHERE user_tg_id=?", (tg_id,)).fetchall()
        conn.close()
        print(f"Info: database/get_orders_by_user_tg_id -> True")
        return orders
    except Exception as e:
        print(f"Error: database/get_orders_by_user_tg_id -> {e}")
        return False


def orders_to_excel(filename, year=False, month=False):
    # try:
        headers= [
        "sana",
        "Buyurtma idsi",
        "Mahsulot nomi",
        "Buyurtmalar soni",
        "Buyurtma narhi",
        "Viloyat",
        "Manzil",
        "Buyurtmachi ismi",
        "Buyuyrtmachi telefon raqami",
        "Izoh"
        ]
        conn = sqlite3.connect(DATABASE_NAME)
        orders = conn.execute("SELECT * FROM orders").fetchall()
        detas = conn.execute("SELECT deta FROM orders").fetchall()
        conn.close()
        workbook = xlsxwriter.Workbook(filename)
        detas_ = []
        for deta in detas:
            if deta[0].split(" ")[0].split("-")[0] == year and deta[0].split(" ")[0].split("-")[1] == \
                    month:detas_.append(
                deta[0].split(" ")[0])
        detas_ = list(set(detas_))
        for deta in detas_:
            worksheet = workbook.add_worksheet(name=deta)
            for i, header in enumerate(headers):
                worksheet.write(0, i, header, workbook.add_format(
                    {
                        'bg_color': '#008066',
                        'font_size': 12,
                        'bold': True,
                        'italic': False,
                    }
                )
                                )
            n = 0
            for d in orders:
                if d[4].split(" ")[0] == deta:
                    n += 1
                    product_ = get_product_all_data_by_id(d[1])
                    user_ = get_user_by_tg_ids(d[5])
                    # print(user_)
                    worksheet.write(n, 0, d[4])
                    worksheet.write(n, 1, d[0])
                    worksheet.write(n, 2, product_[0])
                    worksheet.write(n, 3, d[2])
                    if float(d[2])==float(3): osoni = 2
                    elif float(d[2]==float(2)): osoni = 2
                    else:osoni = float(d[2])
                    worksheet.write(n, 4, f"{float(osoni*float(product_[2]))}")
                    worksheet.write(n, 5, user_["viloyat"])
                    worksheet.write(n, 6, f"{user_['viloyat']} {user_['tuman']} {user_['address']}")
                    worksheet.write(n, 7, user_["name"])
                    worksheet.write(n, 8, f"{user_['phone_number']} {user_['aloqa']}")
                    worksheet.write(n, 9, d[3])

            worksheet.set_column('A:B', 30)
            worksheet.set_column('C:G', 20)
            worksheet.set_column('H:J', 40)
        workbook.close()

        print(f"Info: orders_to_excel -> Orders table exported to {filename}")
        return True
    # except Exception as e:
    #     print(f"Error: orders_to_excel -> {e}")
    #     return False

def get_orders_years() -> list:
    """
    :return: list of years
    """
    try:
        conn = sqlite3.connect(DATABASE_NAME)
        orders = conn.execute("SELECT deta FROM orders").fetchall()
        conn.close()
        return_ = []
        for i in orders:
            return_.append(i[0].split("-")[0])
        return_ = list(set(return_))
        print(f"Info: database/get_orders_by_user_tg_id -> True")
        return return_
    except Exception as e:
        print(f"Error: database/get_orders_by_user_tg_id -> {e}")
        return False


def get_orders_months(year) -> list:
    """
    :return: list of months
    """
    try:
        conn = sqlite3.connect(DATABASE_NAME)
        orders = conn.execute("SELECT deta FROM orders").fetchall()
        conn.close()
        return_ = []
        for i in orders:
            if i[0].split("-")[0] == year:
                return_.append(i[0].split("-")[1])
        return_ = list(set(return_))
        print(f"Info: database/get_orders_by_user_tg_id -> True")
        return return_
    except Exception as e:
        print(f"Error: database/get_orders_by_user_tg_id -> {e}")
        return False


#
#

# create_database()
# add_admin(isim="Jam", familiya='O', telefon="+998", aloqa='t.me/mal_un', tg_id='208')
# add_category('cat1')
# add_category('cat2')
# add_category('cat3')
