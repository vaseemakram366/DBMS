# Search a student

import sqlite3

conn = sqlite3.connect("college.db")
cursor = conn.cursor()

name = input("Enter student name: ")

cursor.execute(
    "SELECT * FROM students WHERE name = ?",
    (name,)
)

result = cursor.fetchall()

for row in result:
    print(row)

conn.close()