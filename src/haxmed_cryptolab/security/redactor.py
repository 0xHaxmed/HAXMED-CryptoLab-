"""Redaction and privacy-enforcing helpers."""

import re
from typing import Any, Dict

_PEM_PRIVATE_PATTERN = re.compile(
    r"-----BEGIN (?:RSA )?PRIVATE KEY-----[\s\S]+?-----END (?:RSA )?PRIVATE KEY-----", re.MULTILINE
)
_HEX_KEY_PATTERN = re.compile(r"\b[0-9a-fA-F]{32,128}\b")


def redact_sensitive_string(text: str) -> str:
    """Scrub private keys and raw hex key material from logs and error messages."""
    if not text:
        return ""
    # Mask PEM private keys
    redacted = _PEM_PRIVATE_PATTERN.sub("[REDACTED_PRIVATE_KEY]", text)
    return redacted


def sanitize_audit_metadata(metadata: Dict[str, Any]) -> Dict[str, Any]:
    """Ensure no secret keys or raw plaintexts leak into history metadata."""
    safe_copy = {}
    for k, v in metadata.items():
        lower_k = k.lower()
        if any(
            secret_term in lower_k
            for secret_term in ("key", "plaintext", "password", "candidate", "secret")
        ):
            safe_copy[k] = "[REDACTED]"
        elif isinstance(v, str):
            safe_copy[k] = redact_sensitive_string(v)
        else:
            safe_copy[k] = v
    return safe_copy
