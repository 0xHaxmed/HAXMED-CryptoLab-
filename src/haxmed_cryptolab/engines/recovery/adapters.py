"""Adapters for verifying candidate passwords against target hashes."""

import hashlib
import hmac
from abc import ABC, abstractmethod

import bcrypt
from argon2 import PasswordHasher
from argon2.exceptions import VerificationError, VerifyMismatchError

from haxmed_cryptolab.core.exceptions import ValidationError


class BaseHashAdapter(ABC):
    """Abstract base adapter for hash candidate verification."""

    @property
    @abstractmethod
    def name(self) -> str:
        """Name of the adapter."""
        pass

    @abstractmethod
    def validate_target(self, target: str) -> None:
        """Validate that the target format is compatible with this adapter."""
        pass

    @abstractmethod
    def verify(self, candidate: str, target: str) -> bool:
        """Verify if candidate matches target hash."""
        pass


class RawDigestAdapter(BaseHashAdapter):
    """Verifies unsalted hexadecimal digests using standard cryptographic hash functions."""

    def __init__(self, algorithm: str = "SHA-256"):
        self.algorithm = algorithm.upper()
        self._hash_fn = {
            "SHA-256": hashlib.sha256,
            "SHA-512": hashlib.sha512,
            "MD5": hashlib.md5,
            "SHA-1": hashlib.sha1,
        }.get(self.algorithm)

        if not self._hash_fn:
            raise ValidationError(f"RawDigestAdapter does not support algorithm '{algorithm}'.")

    @property
    def name(self) -> str:
        return f"Raw {self.algorithm}"

    def validate_target(self, target: str) -> None:
        cleaned = target.strip().lower()
        expected_lens = {"SHA-256": 64, "SHA-512": 128, "MD5": 32, "SHA-1": 40}
        expected = expected_lens[self.algorithm]
        if len(cleaned) != expected:
            raise ValidationError(
                f"Target hash for {self.algorithm} must be {expected} hexadecimal characters. "
                f"Received {len(cleaned)} characters."
            )

    def verify(self, candidate: str, target: str) -> bool:
        computed = self._hash_fn(candidate.encode("utf-8")).hexdigest()
        # Constant-time comparison
        return hmac.compare_digest(computed.lower(), target.strip().lower())


class BcryptAdapter(BaseHashAdapter):
    """Verifies candidate passwords against Blowfish-based Bcrypt hashes."""

    @property
    def name(self) -> str:
        return "Bcrypt"

    def validate_target(self, target: str) -> None:
        cleaned = target.strip()
        if not cleaned.startswith(("$2a$", "$2b$", "$2y$")):
            raise ValidationError(
                "Target must be a valid Bcrypt hash starting with $2a$, $2b$, or $2y$."
            )
        if len(cleaned) < 59:
            raise ValidationError("Target Bcrypt hash appears truncated or malformed.")

    def verify(self, candidate: str, target: str) -> bool:
        try:
            cand_bytes = candidate.encode("utf-8")
            target_bytes = target.strip().encode("ascii")
            return bcrypt.checkpw(cand_bytes, target_bytes)
        except Exception:
            return False


class Argon2idAdapter(BaseHashAdapter):
    """Verifies candidate passwords against Argon2id memory-hard hashes."""

    def __init__(self):
        self._ph = PasswordHasher()

    @property
    def name(self) -> str:
        return "Argon2id"

    def validate_target(self, target: str) -> None:
        cleaned = target.strip()
        if not cleaned.startswith("$argon2"):
            raise ValidationError(
                "Target must be a valid Argon2 hash string starting with $argon2."
            )

    def verify(self, candidate: str, target: str) -> bool:
        try:
            return self._ph.verify(target.strip(), candidate)
        except (VerifyMismatchError, VerificationError):
            return False
        except Exception:
            return False
