"""RSA-OAEP Asymmetric Encryption Engine."""

import base64
from typing import Tuple

from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding, rsa
from cryptography.hazmat.primitives.serialization import (
    Encoding,
    NoEncryption,
    PrivateFormat,
    PublicFormat,
    load_pem_private_key,
    load_pem_public_key,
)

from haxmed_cryptolab.core.constants import RSA_DEFAULT_KEY_SIZE, RSA_KEY_SIZES
from haxmed_cryptolab.core.exceptions import CryptographicError, InvalidKeyError, ValidationError

DESCRIPTION = (
    "RSA-OAEP (Optimal Asymmetric Encryption Padding) is the modern standard for public-key encryption. "
    "It uses a randomized Feistel network padding scheme that provides provable security against chosen-ciphertext attacks (IND-CCA2)."
)
LIMITATION_WARNING = (
    "PLAINTEXT SIZE LIMIT: Asymmetric encryption is mathematically constrained by key size. "
    "For RSA-2048 with SHA-256 OAEP padding, the maximum plaintext size is 190 bytes (256 - 2*32 - 2). "
    "In production, asymmetric keys encrypt symmetric session keys (hybrid encryption) rather than bulk data."
)


class RSAOAEPEngine:
    """RSA Public Key Encryption with OAEP Padding."""

    @staticmethod
    def generate_key_pair(key_size: int = RSA_DEFAULT_KEY_SIZE) -> Tuple[str, str]:
        """
        Generate an RSA key pair of the specified bit length.
        Returns (private_key_pem, public_key_pem).
        """
        if key_size not in RSA_KEY_SIZES:
            raise ValidationError(
                f"Unsupported RSA key size: {key_size}. Supported sizes are: {RSA_KEY_SIZES}"
            )

        private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=key_size,
        )
        public_key = private_key.public_key()

        private_pem = private_key.private_bytes(
            encoding=Encoding.PEM,
            format=PrivateFormat.PKCS8,
            encryption_algorithm=NoEncryption(),
        ).decode("utf-8")

        public_pem = public_key.public_bytes(
            encoding=Encoding.PEM,
            format=PublicFormat.SubjectPublicKeyInfo,
        ).decode("utf-8")

        return private_pem, public_pem

    @staticmethod
    def load_public_key(pem_str: str) -> rsa.RSAPublicKey:
        """Parse and validate an RSA public key in PEM format."""
        if not pem_str or not isinstance(pem_str, str):
            raise InvalidKeyError("Public key PEM must be a non-empty string.")
        try:
            key = load_pem_public_key(pem_str.strip().encode("utf-8"))
            if not isinstance(key, rsa.RSAPublicKey):
                raise InvalidKeyError("The provided PEM key is not an RSA public key.")
            return key
        except Exception as e:
            raise InvalidKeyError(f"Failed to load RSA public key: {e}")

    @staticmethod
    def load_private_key(pem_str: str, password: str = None) -> rsa.RSAPrivateKey:
        """Parse and validate an RSA private key in PEM format."""
        if not pem_str or not isinstance(pem_str, str):
            raise InvalidKeyError("Private key PEM must be a non-empty string.")
        pwd_bytes = password.encode("utf-8") if password else None
        try:
            key = load_pem_private_key(pem_str.strip().encode("utf-8"), password=pwd_bytes)
            if not isinstance(key, rsa.RSAPrivateKey):
                raise InvalidKeyError("The provided PEM key is not an RSA private key.")
            return key
        except Exception as e:
            raise InvalidKeyError(f"Failed to load RSA private key: {e}")

    @classmethod
    def get_max_plaintext_bytes(cls, public_key: rsa.RSAPublicKey) -> int:
        """Calculate the maximum allowed plaintext size for OAEP with SHA-256."""
        modulus_bytes = public_key.key_size // 8
        # OAEP with SHA-256: overhead is 2 * hLen + 2 = 2 * 32 + 2 = 66 bytes
        return modulus_bytes - 66

    @classmethod
    def encrypt(cls, plaintext: str, public_key_pem: str) -> str:
        """
        Encrypt plaintext with RSA-OAEP using SHA-256.
        Returns base64-encoded ciphertext.
        """
        pub_key = cls.load_public_key(public_key_pem)
        pt_bytes = plaintext.encode("utf-8")
        max_bytes = cls.get_max_plaintext_bytes(pub_key)

        if len(pt_bytes) > max_bytes:
            raise ValidationError(
                f"Plaintext too long for {pub_key.key_size}-bit RSA-OAEP-SHA256. "
                f"Maximum allowed is {max_bytes} bytes, received {len(pt_bytes)} bytes. "
                "For bulk data, use symmetric encryption or a larger key."
            )

        try:
            ciphertext = pub_key.encrypt(
                pt_bytes,
                padding.OAEP(
                    mgf=padding.MGF1(algorithm=hashes.SHA256()),
                    algorithm=hashes.SHA256(),
                    label=None,
                ),
            )
            return base64.b64encode(ciphertext).decode("ascii")
        except Exception as e:
            raise CryptographicError(f"RSA encryption failed: {e}")

    @classmethod
    def decrypt(cls, ciphertext_b64: str, private_key_pem: str) -> str:
        """
        Decrypt base64-encoded ciphertext using RSA private key.
        Returns UTF-8 plaintext.
        """
        priv_key = cls.load_private_key(private_key_pem)
        try:
            ct_bytes = base64.b64decode(ciphertext_b64.strip())
        except Exception as e:
            raise ValidationError(f"Invalid Base64 ciphertext encoding: {e}")

        try:
            pt_bytes = priv_key.decrypt(
                ct_bytes,
                padding.OAEP(
                    mgf=padding.MGF1(algorithm=hashes.SHA256()),
                    algorithm=hashes.SHA256(),
                    label=None,
                ),
            )
            return pt_bytes.decode("utf-8")
        except Exception as e:
            raise CryptographicError(
                f"RSA decryption failed. Ensure the matching private key is provided and ciphertext is intact: {e}"
            )
