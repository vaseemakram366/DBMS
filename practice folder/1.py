# Creating database

import sqlite3

# database file banegi
conn = sqlite3.connect("college.db")

print("Database created")

conn.close()