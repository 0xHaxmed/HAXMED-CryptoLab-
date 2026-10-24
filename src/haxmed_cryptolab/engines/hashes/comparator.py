"""Constant-time cryptographic digest comparator."""

import hmac
import re
from typing import Optional

from haxmed_cryptolab.models import HashCompareResult

_HEX_REGEX = re.compile(r"^[0-9a-fA-F]+$")


class HashComparator:
    """Performs constant-time hash verification and format validation."""

    @staticmethod
    def is_valid_hex_digest(digest: str) -> bool:
        """Check if string is a non-empty, even-length hexadecimal string."""
        if not digest or not isinstance(digest, str):
            return False
        cleaned = digest.strip().replace(" ", "").replace(":", "")
        return len(cleaned) > 0 and len(cleaned) % 2 == 0 and bool(_HEX_REGEX.match(cleaned))

    @classmethod
    def compare(
        cls,
        digest_a: str,
        digest_b: str,
        expected_algo: Optional[str] = None,
    ) -> HashCompareResult:
        """
        Compare two digest strings in constant time.
        Returns a structured HashCompareResult with MATCH, NO MATCH, or INVALID INPUT.
        """
        raw_a = digest_a.strip().replace(" ", "").replace(":", "").lower()
        raw_b = digest_b.strip().replace(" ", "").replace(":", "").lower()

        if not cls.is_valid_hex_digest(raw_a) or not cls.is_valid_hex_digest(raw_b):
            return HashCompareResult(
                is_match=False,
                status_label="INVALID INPUT",
                digest_a=raw_a,
                digest_b=raw_b,
                algorithm=expected_algo,
                details="One or both supplied values are not valid hexadecimal digests.",
            )

        # Constant-time comparison prevents timing side-channels
        match = hmac.compare_digest(raw_a, raw_b)

        if match:
            details = "Digests match exactly in length and byte content."
            status = "MATCH"
        else:
            details = "Digests differ. The input files or plaintexts are not identical under this hash function."
            status = "NO MATCH"

        return HashCompareResult(
            is_match=match,
            status_label=status,
            digest_a=raw_a,
            digest_b=raw_b,
            algorithm=expected_algo,
            details=details,
        )
