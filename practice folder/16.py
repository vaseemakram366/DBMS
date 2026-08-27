# Create Table + Insert Multiple Records

import sqlite3

conn = sqlite3.connect("college.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS students (
    id INTEGER PRIMARY KEY,
    name TEXT,
    marks INTEGER,
    course TEXT
)
""")

students = [
    (1, "Aman", 85, "CSE"),
    (2, "Rahul", 72, "CSE"),
    (3, "Vaseem", 91, "AI"),
    (4, "Ali", 68, "ECE")
]

cursor.executemany(
    "INSERT OR IGNORE INTO students VALUES (?, ?, ?, ?)",
    students
)

conn.commit()
conn.close()

print("Records inserted!")