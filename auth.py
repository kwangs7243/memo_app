from db import db_connect
def check_id_duplication(user_id):
    conn = db_connect()
    cursor = conn.cursor()
    sql = "SELECT user_id From user_info WHERE user_id = %s"
    cursor.execute(sql, (user_id,))
    result = cursor.fetchone()
    conn.close()
    if result:
        return True
    else:
        return False
def sign_up(user_id, password):
    conn = db_connect()
    cursor = conn.cursor()
    sql = "INSERT INTO user_info (user_id, user_pw) VALUES (%s, %s)"
    cursor.execute(sql, (user_id, password))
    conn.commit()
    conn.close()
def sign_in(user_id, password):
    conn = db_connect()
    cursor = conn.cursor()
    sql = "SELECT user_id From user_info WHERE user_id = %s AND user_pw = %s"
    cursor.execute(sql, (user_id, password))
    result = cursor.fetchone()
    conn.close()
    if result:
        return True
    else:
        return False
def get_user_id(user_id):
    conn = db_connect()
    cursor = conn.cursor()
    sql = "SELECT id From user_info WHERE user_id = %s"
    cursor.execute(sql, (user_id,))
    result = cursor.fetchone()
    conn.close()
    if result:
        return result["id"]
    else:
        return None
