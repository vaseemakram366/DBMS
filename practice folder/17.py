# Transaction — COMMIT & ROLLBACK

import sqlite3

conn = sqlite3.connect("bank.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS account (
    id INTEGER PRIMARY KEY,
    name TEXT,
    balance REAL
)
""")

cursor.execute("INSERT OR IGNORE INTO account VALUES (1, 'Aman', 5000)")
cursor.execute("INSERT OR IGNORE INTO account VALUES (2, 'Rahul', 3000)")

try:
    # Transfer 1000 from Aman to Rahul
    cursor.execute(
        "UPDATE account SET balance = balance - ? WHERE id = ?",
        (1000, 1)
    )

    cursor.execute(
        "UPDATE account SET balance = balance + ? WHERE id = ?",
        (1000, 2)
    )

    conn.commit()
    print("Transaction successful!")

except Exception as e:
    conn.rollback()
    print("Transaction failed:", e)

conn.close()