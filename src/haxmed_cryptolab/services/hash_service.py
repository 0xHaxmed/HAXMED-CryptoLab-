"""Service coordinating cryptographic hash operations."""

import time
from pathlib import Path
from typing import Callable, List, Optional

from haxmed_cryptolab.core.config import ConfigManager
from haxmed_cryptolab.engines.hashes.comparator import HashComparator
from haxmed_cryptolab.engines.hashes.hasher import HashEngine
from haxmed_cryptolab.engines.hashes.identifier import HashIdentifier
from haxmed_cryptolab.models import HashCompareResult, HashIdentificationCandidate, HashResult
from haxmed_cryptolab.storage.history_repository import HistoryRepository


class HashService:
    """Coordinates hash calculation, verification, and identification."""

    def __init__(
        self,
        history_repo: Optional[HistoryRepository] = None,
        config_mgr: Optional[ConfigManager] = None,
    ):
        self.history_repo = history_repo or HistoryRepository()
        self.config_mgr = config_mgr or ConfigManager()

    def _log_audit(
        self, operation: str, algorithm: str, status: str, duration_ms: float, details: str = ""
    ):
        if self.config_mgr.config.enable_history:
            self.history_repo.add_record(
                operation_type=operation,
                algorithm=algorithm,
                status=status,
                duration_ms=duration_ms,
                details=details,
            )

    def hash_text(self, text: str, algorithm: str) -> HashResult:
        """Compute digest for text input."""
        t0 = time.perf_counter()
        digest = HashEngine.hash_text(text, algorithm)
        dt_ms = (time.perf_counter() - t0) * 1000
        self._log_audit("HASH_TEXT", algorithm, "SUCCESS", dt_ms, f"Len={len(text)} chars")
        return HashResult(
            algorithm=algorithm,
            digest_hex=digest,
            input_type="TEXT",
            execution_time_ms=dt_ms,
        )

    def hash_file(
        self,
        file_path: str,
        algorithm: str,
        chunk_size_kb: int = 64,
        progress_callback: Optional[Callable[[int, int], None]] = None,
        cancel_check: Optional[Callable[[], bool]] = None,
    ) -> HashResult:
        """Compute digest for a file on disk using streaming reads."""
        t0 = time.perf_counter()
        path = Path(file_path).resolve()
        file_size = path.stat().st_size if path.exists() else 0

        digest = HashEngine.hash_file(
            file_path=str(path),
            algorithm=algorithm,
            chunk_size_bytes=chunk_size_kb * 1024,
            progress_callback=progress_callback,
            cancel_check=cancel_check,
        )
        dt_ms = (time.perf_counter() - t0) * 1000
        self._log_audit(
            "HASH_FILE", algorithm, "SUCCESS", dt_ms, f"File={path.name}, Size={file_size}B"
        )
        return HashResult(
            algorithm=algorithm,
            digest_hex=digest,
            input_type="FILE",
            file_path=str(path),
            file_size_bytes=file_size,
            execution_time_ms=dt_ms,
        )

    def compare_digests(
        self,
        digest_a: str,
        digest_b: str,
        algorithm: Optional[str] = None,
    ) -> HashCompareResult:
        """Compare two hexadecimal digest strings in constant time."""
        result = HashComparator.compare(digest_a, digest_b, algorithm)
        status = "MATCH" if result.is_match else result.status_label
        self._log_audit("COMPARE_HASHES", algorithm or "UNKNOWN", status, 0.0, result.details)
        return result

    def identify_format(self, hash_str: str) -> List[HashIdentificationCandidate]:
        """Analyze format and provide cautious candidate interpretations."""
        candidates = HashIdentifier.identify(hash_str)
        top = candidates[0].algorithm if candidates else "Unknown"
        self._log_audit("IDENTIFY_HASH", top, "SUCCESS", 0.0, f"Found {len(candidates)} candidates")
        return candidates
