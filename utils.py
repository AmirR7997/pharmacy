class MenuStack:

    def __init__(self, default_menu):
        self.elements = list()
        self.default_menu = default_menu

    def push(self, element):
        self.elements.append(element)

    def pop(self):
        if len(self.elements) == 0:
            return self.default_menu

        popped_element = self.elements[-1]
        del self.elements[-1]
        return popped_element

    def top(self):
        if len(self.elements) == 0:
            return self.default_menu
        return self.elements[-1]
    def __str__(self):
        return str(self.elements)

from constant import set_integer_flag_sql, get_illnes_sql, get_recipy_sql, update_user_filed_sql, get_integer_flag_sql
import sqlite3


def set_integer_flag(value, column_name, table_name, chat_id):
    sql = set_integer_flag_sql(value, column_name, table_name, chat_id)

    conn = sqlite3.connect("pharmacy_db")
    cursor = conn.cursor()
    cursor.execute(sql)
    conn.commit()

def check_illnes(chat_id):
    try:
        sql = get_illnes_sql(chat_id)
        conn = sqlite3.connect("pharmacy_db")
        cursor = conn.cursor()

        cursor.execute(sql)
        conn.commit()
        result = cursor.fetchone()
        if result is not None:
            return True
        return False
    except Exception as e:
        print("Database error")
        print(e)

def check_recipy(chat_id):
    try:
        sql = get_recipy_sql(chat_id)
        conn = sqlite3.connect("pharmacy_db")
        cursor = conn.cursor()

        cursor.execute(sql)
        conn.commit()
        result = cursor.fetchone()
        if result is not None:
            return True
        return False
    except Exception as e:
        print("Database error")
        print(e)

def update_user_filed(chat_id, filed_name, value):
    sql = update_user_filed_sql(chat_id, filed_name, value)

    conn = sqlite3.connect("pharmacy_db")
    cursor = conn.cursor()
    cursor.execute(sql)
    conn.commit()

def get_integer_flag(column_name, table_name, chat_id):
    sql = get_integer_flag_sql(column_name, table_name, chat_id)
    conn = sqlite3.connect("pharmacy_db")
    cursor = conn.cursor()
    cursor.execute(sql)
    conn.commit()

    flag = cursor.fetchall()
    flag = flag[0][0]

    return flag