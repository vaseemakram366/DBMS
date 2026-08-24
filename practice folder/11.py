# Insert multiple records

import sqlite3

conn = sqlite3.connect("college.db")
cursor = conn.cursor()

students = [
    ("Vaseem", 20, 85),
    ("Rahul", 21, 78),
    ("Aman", 20, 92),
    ("Priya", 21, 88)
]

cursor.executemany("""
INSERT INTO students (name, age, marks)
VALUES (?, ?, ?)
""", students)

conn.commit()
conn.close()

print("Records inserted!")