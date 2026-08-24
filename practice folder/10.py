# Insert data

import sqlite3

conn = sqlite3.connect("college.db")
cursor = conn.cursor()

cursor.execute("""
INSERT INTO students (name, age, marks)
VALUES ('Vaseem', 20, 85)
""")

conn.commit()
conn.close()

print("Data inserted successfully!")