import sqlite3
from pathlib import Path

# Database file location
DATABASE_PATH = Path(__file__).resolve().parent / "tasks.db"


def get_connection():
    connection = sqlite3.connect(DATABASE_PATH)
    connection.row_factory = sqlite3.Row
    return connection


def initialize_database():

    connection = get_connection()

    try:
        cursor = connection.cursor()

        # Create tasks table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                done INTEGER NOT NULL DEFAULT 0
            )
        """)

        # Check whether sample tasks already exist
        cursor.execute("SELECT COUNT(*) FROM tasks")
        task_count = cursor.fetchone()[0]

        # Insert sample tasks only when the table is empty
        if task_count == 0:
            sample_tasks = [
                ("Complete Python assignment", 0),
                ("Learn FastAPI", 0),
                ("Update GitHub profile", 1)
            ]

            cursor.executemany(
                "INSERT INTO tasks (title, done) VALUES (?, ?)",
                sample_tasks
            )

        connection.commit()

    finally:
        connection.close()