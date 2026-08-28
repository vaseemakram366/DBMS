# JOIN — Multiple Tables

import sqlite3

conn = sqlite3.connect("college.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS students (
    student_id INTEGER PRIMARY KEY,
    name TEXT,
    dept_id INTEGER
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS departments (
    dept_id INTEGER PRIMARY KEY,
    dept_name TEXT
)
""")

cursor.execute("""
SELECT students.student_id,
       students.name,
       departments.dept_name
FROM students
INNER JOIN departments
ON students.dept_id = departments.dept_id
""")

for row in cursor.fetchall():
    print(row)

conn.close()