def create_new_user_query(id):
    sql = f"INSERT INTO user (id) VALUES ({id})"
    return sql

def set_integer_flag_sql(value, column_name, table_name, chat_id):
    sql = f"UPDATE {table_name} SET {column_name} = {value} WHERE id = {chat_id}"
    return sql

def get_illnes_sql(chat_id):
    sql = f"""SELECT illnes
              FROM user 
              WHERE id = {chat_id}"""
    return sql

def get_recipy_sql(chat_id):
    sql = f"""SELECT recipy
              FROM user
              WHERE id = {chat_id}"""
    return sql