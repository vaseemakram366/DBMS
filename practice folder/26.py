# Indexing

import sqlite3

conn = sqlite3.connect("college.db")
cursor = conn.cursor()

cursor.execute("""
CREATE INDEX IF NOT EXISTS idx_student_name
ON students(name)
""")

conn.commit()

print("Index created successfully!")

conn.close()