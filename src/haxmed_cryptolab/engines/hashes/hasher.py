"""Cryptographic hash calculation engine for text and chunked files."""

import hashlib
from typing import Callable, Optional

from haxmed_cryptolab.core.exceptions import (
    FileOperationError,
    UnsupportedAlgorithmError,
    ValidationError,
)
from haxmed_cryptolab.security.validator import validate_file_path

ALGO_MAP = {
    "SHA-256": hashlib.sha256,
    "SHA-512": hashlib.sha512,
    "SHA3-256": hashlib.sha3_256,
    "SHA3-512": hashlib.sha3_512,
    "MD5": hashlib.md5,
    "SHA-1": hashlib.sha1,
}


class HashEngine:
    """Hash computation engine."""

    @staticmethod
    def get_hash_constructor(algorithm: str) -> Callable[[], "hashlib._Hash"]:
        """Retrieve the hashlib constructor for the selected algorithm."""
        normalized = algorithm.strip().upper()
        if normalized not in ALGO_MAP:
            raise UnsupportedAlgorithmError(
                f"Unsupported algorithm '{algorithm}'. Supported: {list(ALGO_MAP.keys())}"
            )
        return ALGO_MAP[normalized]

    @classmethod
    def hash_text(cls, text: str, algorithm: str) -> str:
        """Compute the hexadecimal digest of a UTF-8 string."""
        if text is None:
            raise ValidationError("Text input cannot be None.")
        constructor = cls.get_hash_constructor(algorithm)
        h = constructor()
        h.update(text.encode("utf-8"))
        return h.hexdigest()

    @classmethod
    def hash_file(
        cls,
        file_path: str,
        algorithm: str,
        chunk_size_bytes: int = 65536,
        progress_callback: Optional[Callable[[int, int], None]] = None,
        cancel_check: Optional[Callable[[], bool]] = None,
    ) -> str:
        """
        Compute the hexadecimal digest of a file using chunked streaming reads.
        Ensures memory footprint remains minimal regardless of file size.
        """
        path = validate_file_path(file_path, must_exist=True)
        total_size = path.stat().st_size
        bytes_read = 0

        constructor = cls.get_hash_constructor(algorithm)
        h = constructor()

        try:
            with open(path, "rb") as f:
                while True:
                    if cancel_check and cancel_check():
                        raise InterruptedError("File hashing was cancelled by user.")

                    chunk = f.read(chunk_size_bytes)
                    if not chunk:
                        break
                    h.update(chunk)
                    bytes_read += len(chunk)

                    if progress_callback and total_size > 0:
                        progress_callback(bytes_read, total_size)
        except (IOError, OSError) as e:
            raise FileOperationError(f"Error reading file '{path}': {e}")

        return h.hexdigest()
