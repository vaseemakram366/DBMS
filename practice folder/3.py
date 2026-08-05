# Inserting a record

import sqlite3

conn = sqlite3.connect("college.db")
cur = conn.cursor()

cur.execute("INSERT INTO students (name, age) VALUES (?, ?)",
            ("Vaseem", 22))

conn.commit()
print("Data inserted")

conn.close()