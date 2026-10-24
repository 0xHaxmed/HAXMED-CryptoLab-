"""Vigenère Cipher engine."""

from haxmed_cryptolab.core.exceptions import ValidationError

DESCRIPTION = (
    "The Vigenère Cipher is a polyalphabetic substitution cipher described by Giovan Battista Bellaso "
    "and later misattributed to Blaise de Vigenère. It encrypts alphabetic text using a repeating keyword, "
    "where each letter defines a Caesar shift."
)
TRANSFORMATION_EXPLANATION = (
    "Encryption: C[i] = (P[i] + K[i mod len(K)]) mod 26\n"
    "Decryption: P[i] = (C[i] - K[i mod len(K)]) mod 26\n"
    "Non-alphabetic characters are preserved and do not advance the keyword position."
)
SECURITY_WARNING = (
    "INSECURE: Although historically deemed 'le chiffre indéchiffrable' (the indecipherable cipher), "
    "Vigenère is easily broken via Kasiski examination and index of coincidence analysis, "
    "which reveal key length followed by Caesar frequency solving."
)


class VigenereCipher:
    """Vigenère Cipher implementation."""

    @staticmethod
    def validate_key(key: str) -> str:
        """Validate that the key contains alphabetic characters."""
        if not key or not isinstance(key, str):
            raise ValidationError("Vigenère key must be a non-empty string.")
        cleaned = "".join([c.upper() for c in key if c.isalpha()])
        if not cleaned:
            raise ValidationError("Vigenère key must contain at least one alphabetic letter (A-Z).")
        return cleaned

    @classmethod
    def encrypt(cls, plaintext: str, key: str) -> str:
        """Encrypt plaintext using the Vigenère cipher."""
        clean_key = cls.validate_key(key)
        key_len = len(clean_key)
        result = []
        key_idx = 0

        for char in plaintext:
            if "a" <= char <= "z":
                shift = ord(clean_key[key_idx % key_len]) - ord("A")
                result.append(chr((ord(char) - ord("a") + shift) % 26 + ord("a")))
                key_idx += 1
            elif "A" <= char <= "Z":
                shift = ord(clean_key[key_idx % key_len]) - ord("A")
                result.append(chr((ord(char) - ord("A") + shift) % 26 + ord("A")))
                key_idx += 1
            else:
                result.append(char)

        return "".join(result)

    @classmethod
    def decrypt(cls, ciphertext: str, key: str) -> str:
        """Decrypt ciphertext using the Vigenère cipher."""
        clean_key = cls.validate_key(key)
        key_len = len(clean_key)
        result = []
        key_idx = 0

        for char in ciphertext:
            if "a" <= char <= "z":
                shift = ord(clean_key[key_idx % key_len]) - ord("A")
                result.append(chr((ord(char) - ord("a") - shift) % 26 + ord("a")))
                key_idx += 1
            elif "A" <= char <= "Z":
                shift = ord(clean_key[key_idx % key_len]) - ord("A")
                result.append(chr((ord(char) - ord("A") - shift) % 26 + ord("A")))
                key_idx += 1
            else:
                result.append(char)

        return "".join(result)
