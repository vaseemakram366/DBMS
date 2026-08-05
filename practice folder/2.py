# Creating Table

import sqlite3

conn = sqlite3.connect("college.db")
cur = conn.cursor()

cur.execute("""
CREATE TABLE IF NOT EXISTS students (
    id INTEGER PRIMARY KEY,
    name TEXT,
    age INTEGER
)
""")

print("Table created")

conn.commit()
conn.close()