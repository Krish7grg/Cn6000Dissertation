# database.py
# Local SQLite database for users and feedback

import sqlite3


def create_connection():
    """Create a database connection."""
    return sqlite3.connect("frontend_app.db", check_same_thread=False)


conn = create_connection()
cursor = conn.cursor()


def init_db():
    """Create required tables if they do not already exist."""
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            email TEXT UNIQUE,
            password TEXT
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS feedback (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_email TEXT,
            rating INTEGER,
            comments TEXT
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS resume_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_email TEXT,
            template_name TEXT,
            generated_resume TEXT,
            success_rate REAL,
            improvement_rate REAL,
            seniority_level TEXT
        )
    """)

    conn.commit()


init_db()