"""Columnar Transposition Cipher engine."""

import math
from typing import List, Union

from haxmed_cryptolab.core.exceptions import ValidationError

DESCRIPTION = (
    "The Columnar Transposition Cipher is a classical permutation cipher where the order of "
    "characters is rearranged according to a regular grid defined by the key columns."
)
TRANSFORMATION_EXPLANATION = (
    "Encryption: The plaintext is written row-by-row into a grid of 'k' columns. "
    "The ciphertext is read column-by-column.\n"
    "Decryption: Reconstructs the grid dimensions and places the ciphertext back into columns, "
    "then reads out row-by-row."
)
SECURITY_WARNING = (
    "INSECURE: Transposition ciphers do not alter character frequencies. An analyst can easily detect "
    "transposition via single-letter frequency analysis and recover the key by analyzing bigram and "
    "anagram statistics across columns."
)


class TranspositionCipher:
    """Simple Columnar Transposition Cipher."""

    @staticmethod
    def validate_key(key: Union[int, str]) -> int:
        """Validate that the key represents a positive integer column count >= 2."""
        try:
            k = int(key)
        except (ValueError, TypeError):
            raise ValidationError(
                "Transposition key must be a valid integer representing column count."
            )
        if k < 2:
            raise ValidationError("Transposition column count must be at least 2.")
        return k

    @classmethod
    def encrypt(cls, plaintext: str, key: Union[int, str]) -> str:
        """Encrypt plaintext by writing across rows and reading down columns."""
        if not plaintext:
            return ""
        num_cols = cls.validate_key(key)
        if num_cols > len(plaintext):
            # If columns exceed text length, columns 0..len-1 have 1 char each
            num_cols = len(plaintext)

        columns: List[List[str]] = [[] for _ in range(num_cols)]
        for i, char in enumerate(plaintext):
            col_idx = i % num_cols
            columns[col_idx].append(char)

        return "".join("".join(col) for col in columns)

    @classmethod
    def decrypt(cls, ciphertext: str, key: Union[int, str]) -> str:
        """Decrypt ciphertext by reconstructing the grid columns and reading rows."""
        if not ciphertext:
            return ""
        num_cols = cls.validate_key(key)
        total_len = len(ciphertext)
        if num_cols > total_len:
            num_cols = total_len

        num_rows = math.ceil(total_len / num_cols)
        num_full_cols = total_len % num_cols
        if num_full_cols == 0:
            num_full_cols = num_cols

        columns: List[str] = []
        current_idx = 0

        for col in range(num_cols):
            # The first num_full_cols columns have length num_rows, remaining have num_rows - 1
            col_len = num_rows if col < num_full_cols else (num_rows - 1)
            columns.append(ciphertext[current_idx : current_idx + col_len])
            current_idx += col_len

        plaintext = []
        for r in range(num_rows):
            for col in range(num_cols):
                if r < len(columns[col]):
                    plaintext.append(columns[col][r])

        return "".join(plaintext)
