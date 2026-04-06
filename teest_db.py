import pymysql

conn = pymysql.connect(
    host="localhost",
    user="root",        # ← 네 아이디
    password="ezen123!",  # ← 네 비번
    database="memo_app",
    charset="utf8"
)

import pymysql
import datetime as dt

conn = pymysql.connect(
    host="localhost",
    user="root",
    password="ezen123!",
    database="memo_app",
    charset="utf8",
    cursorclass=pymysql.cursors.DictCursor
)

cursor = conn.cursor()

sql = "SELECT * FROM memos"
cursor.execute(sql)
row = cursor.fetchall()
print(row)

conn.close()
