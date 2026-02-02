import sqlite3

DB_PATH = "database/attendance.db"

conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

cursor.execute("DELETE FROM attendance")
cursor.execute("DELETE FROM users")

conn.commit()
conn.close()

print("✅ All database data cleared")
