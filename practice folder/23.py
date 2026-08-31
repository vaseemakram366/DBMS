# Stored-Procedure-like Function in Python

import sqlite3

def get_students_by_marks(min_marks):
    conn = sqlite3.connect("college.db")
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM students WHERE marks >= ?",
        (min_marks,)
    )

    data = cursor.fetchall()

    conn.close()

    return data


students = get_students_by_marks(80)

for student in students:
    print(student)