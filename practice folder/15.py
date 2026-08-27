# Full CRUD Program

import sqlite3

conn = sqlite3.connect("college.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS students (
    id INTEGER PRIMARY KEY,
    name TEXT,
    age INTEGER
)
""")

while True:
    print("\n1. Insert")
    print("2. Display")
    print("3. Update")
    print("4. Delete")
    print("5. Exit")

    choice = input("Enter your choice: ")

    if choice == "1":
        id = int(input("Enter ID: "))
        name = input("Enter Name: ")
        age = int(input("Enter Age: "))

        cursor.execute(
            "INSERT INTO students VALUES (?, ?, ?)",
            (id, name, age)
        )
        conn.commit()
        print("Student added successfully!")

    elif choice == "2":
        cursor.execute("SELECT * FROM students")
        rows = cursor.fetchall()

        for row in rows:
            print(row)

    elif choice == "3":
        id = int(input("Enter Student ID: "))
        age = int(input("Enter New Age: "))

        cursor.execute(
            "UPDATE students SET age = ? WHERE id = ?",
            (age, id)
        )
        conn.commit()
        print("Student updated successfully!")

    elif choice == "4":
        id = int(input("Enter Student ID: "))

        cursor.execute(
            "DELETE FROM students WHERE id = ?",
            (id,)
        )
        conn.commit()
        print("Student deleted successfully!")

    elif choice == "5":
        conn.close()
        print("Database closed!")
        break

    else:
        print("Invalid choice!")
        