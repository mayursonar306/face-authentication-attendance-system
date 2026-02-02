import sqlite3
from datetime import datetime




DB_PATH = "database/attendance.db"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT UNIQUE
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS attendance(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        timestamp TEXT,
        status TEXT
    )
    """)

    conn.commit()
    conn.close()


def add_user(name):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("INSERT OR IGNORE INTO users(name) VALUES(?)", (name,))
    conn.commit()
    conn.close()


def mark_attendance(name, status):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    cursor.execute("""
        INSERT INTO attendance(name, timestamp, status)
        VALUES(?,?,?)
    """, (name, timestamp, status))

    conn.commit()
    conn.close()


def get_last_status(name):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT status FROM attendance
        WHERE name = ?
        ORDER BY timestamp DESC
        LIMIT 1
    """, (name,))

    row = cursor.fetchone()
    conn.close()

    if row:
        return row[0]
    return None

