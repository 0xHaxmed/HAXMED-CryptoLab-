"""Input validation routines for HAXMED CryptoLab."""

import os
from pathlib import Path
from typing import Union

from haxmed_cryptolab.core.exceptions import FileOperationError, ValidationError


def validate_text_input(text: str, max_chars: int = 10_000_000) -> str:
    """Validate that text is provided and within memory limits."""
    if text is None:
        raise ValidationError("Input text cannot be None.")
    if len(text) > max_chars:
        raise ValidationError(f"Input exceeds maximum allowed length of {max_chars} characters.")
    return text


def validate_file_path(path: Union[str, Path], must_exist: bool = True) -> Path:
    """Validate that file path is safe and accessible."""
    if not path:
        raise ValidationError("File path cannot be empty.")
    p = Path(path).resolve()
    if must_exist and not p.is_file():
        raise FileOperationError(f"File not found: {p}")
    if must_exist and not os.access(p, os.R_OK):
        raise FileOperationError(f"File is not readable (check permissions): {p}")
    return p


def validate_hex_string(hex_str: str, expected_len_bytes: int = None) -> bytes:
    """Validate that a string is valid hex and optionally of expected byte length."""
    cleaned = hex_str.strip().replace(" ", "").replace(":", "").lower()
    if not cleaned:
        raise ValidationError("Hexadecimal string cannot be empty.")
    if len(cleaned) % 2 != 0:
        raise ValidationError("Hexadecimal string must have an even number of characters.")
    try:
        raw_bytes = bytes.fromhex(cleaned)
    except ValueError as e:
        raise ValidationError(f"Invalid hexadecimal encoding: {e}")
    if expected_len_bytes is not None and len(raw_bytes) != expected_len_bytes:
        raise ValidationError(
            f"Expected {expected_len_bytes} bytes ({expected_len_bytes * 2} hex chars), "
            f"got {len(raw_bytes)} bytes."
        )
    return raw_bytes
