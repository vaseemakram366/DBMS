# Custom SQL Function

import sqlite3

conn = sqlite3.connect("college.db")

def grade(marks):
    if marks >= 90:
        return "A+"
    elif marks >= 80:
        return "A"
    elif marks >= 70:
        return "B"
    elif marks >= 60:
        return "C"
    else:
        return "F"

conn.create_function("GRADE", 1, grade)

cursor = conn.cursor()

cursor.execute("""
SELECT name, marks, GRADE(marks)
FROM students
""")

for row in cursor.fetchall():
    print(row)

conn.close()