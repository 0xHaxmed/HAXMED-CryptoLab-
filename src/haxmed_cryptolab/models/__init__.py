"""Data transfer objects and schemas."""

from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, Optional


class OperationStatus(str, Enum):
    IDLE = "IDLE"
    RUNNING = "RUNNING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"
    CANCELLED = "CANCELLED"


class CryptoCategory(str, Enum):
    CLASSICAL = "CLASSICAL"
    SYMMETRIC = "SYMMETRIC"
    ASYMMETRIC = "ASYMMETRIC"


class DetectedCategory(str, Enum):
    HASH = "HASH"
    AES_GCM_CONTAINER = "AES_GCM_CONTAINER"
    RSA_CIPHERTEXT = "RSA_CIPHERTEXT"
    PEM_KEY = "PEM_KEY"
    CAESAR_CIPHER = "CAESAR_CIPHER"
    CLASSICAL_SUBSTITUTION = "CLASSICAL_SUBSTITUTION"
    POLYALPHABETIC_CIPHER = "POLYALPHABETIC_CIPHER"
    BASE64_BLOB = "BASE64_BLOB"
    HEX_BLOB = "HEX_BLOB"
    PLAIN_TEXT = "PLAIN_TEXT"
    UNKNOWN = "UNKNOWN"


@dataclass
class DetectionReport:
    """Structured report produced by the Smart Crypto Auto-Detector."""

    category: DetectedCategory
    suggested_algorithm: str
    confidence: str  # "HIGH", "MEDIUM", "LOW"
    summary: str
    details: str
    suggested_action: str  # e.g., "DECRYPT_AES", "DECRYPT_CAESAR", "DECRYPT_RSA", "HASH_WORKBENCH", "RECOVERY_LAB"
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class CryptoResult:
    """Result of a cryptographic transformation."""

    success: bool
    data: str
    algorithm: str
    operation: str  # "ENCRYPT", "DECRYPT", "SIGN", "VERIFY"
    metadata: Dict[str, Any] = field(default_factory=dict)
    error_message: Optional[str] = None
    execution_time_ms: float = 0.0


@dataclass
class HashResult:
    """Result of a cryptographic hash calculation."""

    algorithm: str
    digest_hex: str
    input_type: str  # "TEXT" or "FILE"
    file_path: Optional[str] = None
    file_size_bytes: int = 0
    execution_time_ms: float = 0.0


@dataclass
class HashCompareResult:
    """Result of a hash comparison."""

    is_match: bool
    status_label: str  # "MATCH", "NO MATCH", "INVALID INPUT"
    digest_a: str
    digest_b: str
    algorithm: Optional[str] = None
    details: str = ""


@dataclass
class HashIdentificationCandidate:
    """Possible algorithm interpretation for a hash string."""

    algorithm: str
    bit_length: int
    confidence: str  # "POSSIBLE", "LIKELY"
    notes: str = ""


@dataclass
class RecoveryCandidateMatch:
    """Identified plaintext match in recovery lab."""

    target_hash: str
    plaintext: str
    rule_applied: str
    attempts_evaluated: int
    time_elapsed_seconds: float


@dataclass
class RecoveryProgress:
    """Progress snapshot of recovery worker."""

    attempts: int
    total_candidates: int
    current_candidate: str
    elapsed_seconds: float
    candidates_per_second: float


@dataclass
class HistoryRecord:
    """Sanitized operation audit record (Never contains plaintexts or secret keys!)."""

    id: Optional[int]
    timestamp: str
    operation_type: str
    algorithm: str
    status: str
    duration_ms: float
    details: str
