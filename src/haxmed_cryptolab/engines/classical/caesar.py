"""Caesar Cipher engine and brute-force explorer."""

from typing import List, Tuple

from haxmed_cryptolab.core.exceptions import ValidationError

DESCRIPTION = (
    "The Caesar Cipher is one of the earliest known substitution ciphers, "
    "attributed to Julius Caesar. It shifts each letter in the alphabet by a fixed integer key (1 to 25)."
)
TRANSFORMATION_EXPLANATION = (
    "Encryption: C = (P + k) mod 26\n"
    "Decryption: P = (C - k) mod 26\n"
    "Non-alphabetic characters (spaces, punctuation, digits, Arabic script) are preserved without modification."
)
SECURITY_WARNING = (
    "INSECURE: The Caesar cipher provides zero practical confidentiality. "
    "With only 25 possible keys, it can be broken in microseconds via exhaustive brute-force search "
    "or single-character frequency analysis."
)


class CaesarCipher:
    """Caesar Cipher implementation with shift validation and brute-force exploration."""

    @staticmethod
    def validate_shift(shift: int) -> int:
        """Validate shift is an integer and normalize modulo 26."""
        if not isinstance(shift, int):
            try:
                shift = int(shift)
            except (ValueError, TypeError):
                raise ValidationError("Caesar cipher shift must be a valid integer.")
        return shift % 26

    @classmethod
    def encrypt(cls, plaintext: str, shift: int) -> str:
        """Encrypt plaintext using Caesar cipher with given shift."""
        k = cls.validate_shift(shift)
        result = []
        for char in plaintext:
            if "a" <= char <= "z":
                result.append(chr((ord(char) - ord("a") + k) % 26 + ord("a")))
            elif "A" <= char <= "Z":
                result.append(chr((ord(char) - ord("A") + k) % 26 + ord("A")))
            else:
                result.append(char)
        return "".join(result)

    @classmethod
    def decrypt(cls, ciphertext: str, shift: int) -> str:
        """Decrypt ciphertext using Caesar cipher with given shift."""
        k = cls.validate_shift(shift)
        return cls.encrypt(ciphertext, -k)

    @classmethod
    def brute_force(cls, ciphertext: str) -> List[Tuple[int, str]]:
        """Return all 25 possible decryptions with their corresponding shift keys."""
        candidates = []
        for shift in range(1, 26):
            decrypted = cls.decrypt(ciphertext, shift)
            candidates.append((shift, decrypted))
        return candidates
