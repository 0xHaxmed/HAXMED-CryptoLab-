"""Service managing history inspection and audit report exports."""

import json
from datetime import datetime
from typing import List, Optional

from haxmed_cryptolab.core.config import ConfigManager
from haxmed_cryptolab.models import HistoryRecord
from haxmed_cryptolab.storage.history_repository import HistoryRepository


class HistoryService:
    """Provides history record queries and sanitized report generation."""

    def __init__(
        self,
        history_repo: Optional[HistoryRepository] = None,
        config_mgr: Optional[ConfigManager] = None,
    ):
        self.history_repo = history_repo or HistoryRepository()
        self.config_mgr = config_mgr or ConfigManager()

    def get_recent_history(self, limit: int = 100) -> List[HistoryRecord]:
        return self.history_repo.get_recent(limit=limit)

    def count_records(self) -> int:
        return self.history_repo.count()

    def clear_history(self) -> None:
        self.history_repo.clear_all()

    def export_history(self, format_type: str = "txt") -> str:
        """Export audit history into formatted TXT or JSON string."""
        records = self.get_recent_history(limit=500)
        timestamp = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")

        if format_type.lower() == "json":
            export_data = {
                "application": "HAXMED CryptoLab",
                "export_timestamp": timestamp,
                "record_count": len(records),
                "privacy_notice": "Zero plaintexts, secret keys, or passwords are stored in history.",
                "records": [
                    {
                        "id": r.id,
                        "timestamp": r.timestamp,
                        "operation": r.operation_type,
                        "algorithm": r.algorithm,
                        "status": r.status,
                        "duration_ms": r.duration_ms,
                        "details": r.details,
                    }
                    for r in records
                ],
            }
            return json.dumps(export_data, indent=2)

        # Plain text
        lines = [
            "=======================================================================",
            "             HAXMED CryptoLab — Operation Audit History",
            "=======================================================================",
            f"Export Date: {timestamp}",
            f"Total Records: {len(records)}",
            "Privacy Notice: All entries are sanitized; no sensitive keys or plaintexts are stored.",
            "-----------------------------------------------------------------------",
            f"{'ID':<6} | {'Timestamp':<23} | {'Operation':<16} | {'Algorithm':<20} | {'Status':<10} | {'Duration (ms)':<13}",
            "-----------------------------------------------------------------------",
        ]
        for r in records:
            lines.append(
                f"{r.id or 0:<6} | {r.timestamp:<23} | {r.operation_type:<16} | {r.algorithm:<20} | {r.status:<10} | {r.duration_ms:<13.2f}"
            )
        lines.append("=======================================================================")
        return "\n".join(lines)
