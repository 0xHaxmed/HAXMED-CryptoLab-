"""Monoalphabetic Substitution Cipher engine."""

import string

from haxmed_cryptolab.core.exceptions import ValidationError

DESCRIPTION = (
    "The Monoalphabetic Substitution Cipher replaces each letter of the plaintext alphabet with a "
    "unique corresponding letter from a 26-character permuted cipher alphabet."
)
TRANSFORMATION_EXPLANATION = (
    "Standard Alphabet: A B C D E F G H I J K L M N O P Q R S T U V W X Y Z\n"
    "Cipher Alphabet:   [User-provided 26 unique character permutation]\n"
    "Each occurrence of letter P is replaced by Cipher[Alphabet.index(P)]. "
    "Case is preserved, and non-alphabetic characters remain untouched."
)
SECURITY_WARNING = (
    "INSECURE: Despite possessing a vast key space (26! ≈ 4 x 10^26), monoalphabetic substitution "
    "completely preserves underlying single-letter frequency distributions and digram patterns, "
    "making it trivially breakable via frequency analysis."
)


class SubstitutionCipher:
    """Monoalphabetic Substitution Cipher implementation."""

    STANDARD_ALPHABET = string.ascii_uppercase

    @staticmethod
    def validate_key(key: str) -> str:
        """Validate that the key is a valid 26-character permutation of the English alphabet."""
        if not key or not isinstance(key, str):
            raise ValidationError("Substitution key must be provided as a string.")
        cleaned = key.strip().upper()
        if len(cleaned) != 26:
            raise ValidationError(
                f"Substitution key must be exactly 26 letters long. Received {len(cleaned)} characters."
            )
        if not cleaned.isalpha():
            raise ValidationError("Substitution key must contain only alphabetic letters (A-Z).")
        if len(set(cleaned)) != 26:
            missing = set(string.ascii_uppercase) - set(cleaned)
            raise ValidationError(
                f"Substitution key must contain 26 UNIQUE letters. Missing: {sorted(list(missing))}"
            )
        return cleaned

    @classmethod
    def encrypt(cls, plaintext: str, key: str) -> str:
        """Encrypt plaintext using the validated 26-letter cipher alphabet."""
        clean_key = cls.validate_key(key)
        upper_map = {src: dst for src, dst in zip(cls.STANDARD_ALPHABET, clean_key)}
        lower_map = {src.lower(): dst.lower() for src, dst in zip(cls.STANDARD_ALPHABET, clean_key)}

        result = []
        for char in plaintext:
            if char in upper_map:
                result.append(upper_map[char])
            elif char in lower_map:
                result.append(lower_map[char])
            else:
                result.append(char)
        return "".join(result)

    @classmethod
    def decrypt(cls, ciphertext: str, key: str) -> str:
        """Decrypt ciphertext using the inverse substitution mapping."""
        clean_key = cls.validate_key(key)
        inv_upper_map = {dst: src for src, dst in zip(cls.STANDARD_ALPHABET, clean_key)}
        inv_lower_map = {
            dst.lower(): src.lower() for src, dst in zip(cls.STANDARD_ALPHABET, clean_key)
        }

        result = []
        for char in ciphertext:
            if char in inv_upper_map:
                result.append(inv_upper_map[char])
            elif char in inv_lower_map:
                result.append(inv_lower_map[char])
            else:
                result.append(char)
        return "".join(result)
