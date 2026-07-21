# database.py
# -----------------------------------------------------------------------------
# This file handles ALL direct interaction with our SQLite database.
# No other file should open a raw sqlite3 connection on its own —
# they should always call the functions defined here.
# -----------------------------------------------------------------------------

import sqlite3

# The name/path of our SQLite database file.
DB_NAME = "database.db"


def get_db_connection():
    """
    Opens and returns a connection to the SQLite database.
    row_factory = sqlite3.Row lets us access columns by NAME (row["name"])
    instead of confusing position (row[0]).
    """
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def init_db():
    """
    Creates the 'students' and 'grades' tables if they don't already exist.
    Safe to call every time the app starts — it will NOT delete existing data.
    """
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            roll_number TEXT NOT NULL UNIQUE
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS grades (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id INTEGER NOT NULL,
            subject TEXT NOT NULL,
            marks REAL NOT NULL CHECK (marks >= 0 AND marks <= 100),
            FOREIGN KEY (student_id) REFERENCES students (id) ON DELETE CASCADE
        )
    """)

    conn.commit()
    conn.close()