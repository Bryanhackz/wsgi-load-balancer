import sqlite3
from contextlib import contextmanager
from pathlib import Path
import time

DB_PATH = Path(__file__).resolve().parent / "lb.db"

@contextmanager
def get_connection():
    conn = sqlite3.connect(DB_PATH, timeout=5.0)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode=WAL;")
    try:
        yield conn
    finally:
        conn.close()

def init_db() -> None:
    with get_connection() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS backends (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                url TEXT UNIQUE NOT NULL,
                is_healthy INTEGER NOT NULL DEFAULT 1,
                last_checked REAL NOT NULL
            )
        """)
        defaults = [
            ("http://127.0.0.1:8001", 1, time.time()),
            ("http://127.0.0.1:8002", 1, time.time()),
            ("http://127.0.0.1:8003", 1, time.time()),
        ]
        for url, health, ts in defaults:
            try:
                conn.execute("INSERT INTO backends (url, is_healthy, last_checked) VALUES (?, ?, ?)", (url, health, ts))
            except sqlite3.IntegrityError:
                pass
        conn.commit()

def get_healthy_backends() -> list[str]:
    with get_connection() as conn:
        rows = conn.execute("SELECT url FROM backends WHERE is_healthy = 1").fetchall()
        return [row["url"] for row in rows]

def update_health(url: str, is_healthy: bool) -> None:
    with get_connection() as conn:
        conn.execute(
            "UPDATE backends SET is_healthy = ?, last_checked = ? WHERE url = ?",
            (1 if is_healthy else 0, time.time(), url)
        )
        conn.commit()
