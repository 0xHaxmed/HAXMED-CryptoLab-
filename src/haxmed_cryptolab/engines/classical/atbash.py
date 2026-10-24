"""Atbash Cipher engine."""

DESCRIPTION = (
    "The Atbash Cipher is a classical monoalphabetic substitution cipher originally developed for the "
    "Hebrew alphabet. It maps the first letter of the alphabet to the last, the second to the penultimate, "
    "and so on (A <-> Z, B <-> Y)."
)
TRANSFORMATION_EXPLANATION = (
    "Transformation: C = (25 - P) mod 26\n"
    "Because the mapping is an involution (its own inverse), the encryption and decryption processes are identical."
)
SECURITY_WARNING = (
    "INSECURE: Atbash possesses a fixed, keyless mapping. Anyone who suspects Atbash can immediately read the plaintext. "
    "It offers zero security."
)


class AtbashCipher:
    """Atbash Cipher implementation."""

    @classmethod
    def transform(cls, text: str) -> str:
        """Apply the Atbash reflection to the input text."""
        result = []
        for char in text:
            if "a" <= char <= "z":
                result.append(chr(ord("z") - (ord(char) - ord("a"))))
            elif "A" <= char <= "Z":
                result.append(chr(ord("Z") - (ord(char) - ord("A"))))
            else:
                result.append(char)
        return "".join(result)

    @classmethod
    def encrypt(cls, plaintext: str) -> str:
        return cls.transform(plaintext)

    @classmethod
    def decrypt(cls, ciphertext: str) -> str:
        return cls.transform(ciphertext)
