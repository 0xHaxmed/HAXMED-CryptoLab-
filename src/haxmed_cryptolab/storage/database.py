"""SQLite connection manager and schema initialization."""

import sqlite3
from pathlib import Path
from typing import Optional

from haxmed_cryptolab.core.constants import DB_PATH

SCHEMA_SQL = """
CREATE TABLE IF NOT EXISTS operation_history (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp TEXT NOT NULL,
    operation_type TEXT NOT NULL,
    algorithm TEXT NOT NULL,
    status TEXT NOT NULL,
    duration_ms REAL NOT NULL,
    details TEXT NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_history_timestamp ON operation_history(timestamp);
"""


class DatabaseManager:
    """Manages SQLite database connections and table lifecycle."""

    def __init__(self, db_path: Optional[Path] = None):
        self.db_path = db_path or DB_PATH
        self.initialize_schema()

    def get_connection(self) -> sqlite3.Connection:
        """Create a connection with row factory enabled."""
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        conn = sqlite3.connect(str(self.db_path))
        conn.row_factory = sqlite3.Row
        return conn

    def initialize_schema(self) -> None:
        """Execute table creation DDL."""
        with self.get_connection() as conn:
            conn.executescript(SCHEMA_SQL)
            conn.commit()
