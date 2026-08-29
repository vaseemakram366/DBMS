# Trigger
import sqlite3

conn = sqlite3.connect("college.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS student_log (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_id INTEGER,
    action TEXT
)
""")

cursor.execute("""
CREATE TRIGGER IF NOT EXISTS student_delete
AFTER DELETE ON students
BEGIN
    INSERT INTO student_log(student_id, action)
    VALUES (OLD.id, 'Student Deleted');
END;
""")

cursor.execute(
    "DELETE FROM students WHERE id = ?",
    (5,)
)

conn.commit()

cursor.execute("SELECT * FROM student_log")

for row in cursor.fetchall():
    print(row)

conn.close()