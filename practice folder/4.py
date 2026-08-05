# Data dekhna (SELECT)

import sqlite3

conn = sqlite3.connect("college.db")
cur = conn.cursor()

cur.execute("SELECT * FROM students")

rows = cur.fetchall()

for row in rows:
    print(row)

conn.close()