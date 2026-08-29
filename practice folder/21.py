# View

import sqlite3

conn = sqlite3.connect("college.db")
cursor = conn.cursor()

cursor.execute("""
CREATE VIEW IF NOT EXISTS high_scorers AS
SELECT id, name, marks
FROM students
WHERE marks >= 80
""")

cursor.execute("SELECT * FROM high_scorers")

for row in cursor.fetchall():
    print(row)

conn.close()