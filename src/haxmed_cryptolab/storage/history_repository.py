"""Privacy-preserving repository for operation history."""

from datetime import datetime
from typing import List, Optional

from haxmed_cryptolab.models import HistoryRecord
from haxmed_cryptolab.security.redactor import redact_sensitive_string
from haxmed_cryptolab.storage.database import DatabaseManager


class HistoryRepository:
    """Manages audit records with strict privacy guarantees."""

    def __init__(self, db_manager: Optional[DatabaseManager] = None):
        self.db = db_manager or DatabaseManager()

    def add_record(
        self,
        operation_type: str,
        algorithm: str,
        status: str,
        duration_ms: float = 0.0,
        details: str = "",
    ) -> int:
        """
        Record a sanitized operation entry.
        Guarantees that sensitive keys and plaintexts are redacted.
        """
        sanitized_details = redact_sensitive_string(details)
        timestamp = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")

        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                INSERT INTO operation_history (timestamp, operation_type, algorithm, status, duration_ms, details)
                VALUES (?, ?, ?, ?, ?, ?)
                """,
                (timestamp, operation_type, algorithm, status, duration_ms, sanitized_details),
            )
            conn.commit()
            return cursor.lastrowid

    def get_recent(self, limit: int = 50) -> List[HistoryRecord]:
        """Fetch the latest history records."""
        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                SELECT id, timestamp, operation_type, algorithm, status, duration_ms, details
                FROM operation_history
                ORDER BY id DESC
                LIMIT ?
                """,
                (limit,),
            )
            rows = cursor.fetchall()
            return [
                HistoryRecord(
                    id=row["id"],
                    timestamp=row["timestamp"],
                    operation_type=row["operation_type"],
                    algorithm=row["algorithm"],
                    status=row["status"],
                    duration_ms=row["duration_ms"],
                    details=row["details"],
                )
                for row in rows
            ]

    def count(self) -> int:
        """Return total number of history records."""
        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM operation_history")
            return cursor.fetchone()[0]

    def clear_all(self) -> None:
        """Purge all history records."""
        with self.db.get_connection() as conn:
            conn.execute("DELETE FROM operation_history")
            conn.commit()
