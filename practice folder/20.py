# GROUP BY + HAVING

import sqlite3

conn = sqlite3.connect("college.db")
cursor = conn.cursor()

cursor.execute("""
SELECT course, COUNT(*) AS total_students
FROM students
GROUP BY course
HAVING COUNT(*) > 1
""")

for row in cursor.fetchall():
    print(row)

conn.close()