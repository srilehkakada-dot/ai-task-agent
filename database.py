"""
database.py
Handles all SQLite operations for storing and retrieving tasks.
"""

import sqlite3
from datetime import datetime

DB_NAME = "tasks.db"


def init_db():
    """Create the tasks table if it doesn't already exist."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            priority TEXT NOT NULL,
            deadline TEXT,
            status TEXT DEFAULT 'pending',
            created_at TEXT
        )
    """)
    conn.commit()
    conn.close()


def add_task(title: str, priority: str = "Medium", deadline: str = "Not specified"):
    """Insert a new task into the database."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO tasks (title, priority, deadline, status, created_at) VALUES (?, ?, ?, ?, ?)",
        (title, priority, deadline, "pending", datetime.now().strftime("%Y-%m-%d %H:%M"))
    )
    conn.commit()
    conn.close()
    return f"Task added: '{title}' (Priority: {priority}, Deadline: {deadline})"


def get_all_tasks():
    """Fetch all tasks from the database."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT id, title, priority, deadline, status FROM tasks ORDER BY id DESC")
    rows = cursor.fetchall()
    conn.close()
    return rows


def update_task_status(task_id: int, status: str):
    """Mark a task as completed or pending."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("UPDATE tasks SET status = ? WHERE id = ?", (status, task_id))
    conn.commit()
    conn.close()


def delete_task(task_id: int):
    """Remove a task from the database."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
    conn.commit()
    conn.close()


def clear_all_tasks():
    """Wipe all tasks (used for the reset button in the UI)."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM tasks")
    conn.commit()
    conn.close()