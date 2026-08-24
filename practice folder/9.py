# Create a database and table
import sqlite3

# Connect to database
conn = sqlite3.connect("college.db")

# Create cursor
cursor = conn.cursor()

# Create table
cursor.execute("""
CREATE TABLE IF NOT EXISTS students (
    id INTEGER PRIMARY KEY,
    name TEXT,
    age INTEGER,
    marks INTEGER
)
""")

conn.commit()
conn.close()

print("Database and table created successfully!")