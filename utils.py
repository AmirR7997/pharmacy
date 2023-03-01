from constant import set_integer_flag_sql, get_illnes_sql, get_recipy_sql
import sqlite3


def set_integer_flag(value, column_name, table_name, chat_id):
    sql = set_integer_flag_sql(value, column_name, table_name, chat_id)

    conn = sqlite3.connect("Pizza_db")
    cursor = conn.cursor()
    cursor.execute(sql)
    conn.commit()

def check_illnes(chat_id):
    try:
        sql = get_illnes_sql(chat_id)
        conn = sqlite3.connect("Pizza_db")
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
        conn = sqlite3.connect("Pizza_db")
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