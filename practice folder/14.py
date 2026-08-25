# Delete a record
import sqlite3

conn = sqlite3.connect("college.db")
cursor = conn.cursor()

cursor.execute("""
DELETE FROM students
WHERE name = 'Rahul'
""")

conn.commit()
conn.close()

print("Record deleted!")