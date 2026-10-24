"""AES-GCM-256 Authenticated Encryption Engine."""

import base64
import json
import os
from typing import Dict, Tuple

from cryptography.exceptions import InvalidTag
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

from haxmed_cryptolab.core.constants import (
    AES_GCM_KEY_SIZE_BITS,
    AES_GCM_NONCE_SIZE_BYTES,
    AES_GCM_TAG_SIZE_BYTES,
    CONTAINER_FORMAT_VERSION,
)
from haxmed_cryptolab.core.exceptions import AuthenticationError, InvalidKeyError, ValidationError

DESCRIPTION = (
    "AES-GCM (Advanced Encryption Standard in Galois/Counter Mode) is a NIST-standardized "
    "Authenticated Encryption with Associated Data (AEAD) cipher. It provides high-performance "
    "confidentiality, integrity, and authenticity verification in a single cryptographic pass."
)
SECURITY_EXPLANATION = (
    "AES-GCM combines CTR mode encryption with GHASH message authentication. "
    "Crucial invariant: NEVER reuse a (Key, Nonce) pair. Reusing a nonce destroys authentication guarantees "
    "and allows key recovery attacks. HAXMED CryptoLab automatically generates a cryptographically "
    "secure 96-bit random nonce for every encryption operation."
)


class AESGCMEngine:
    """AES-GCM-256 authenticated encryption engine."""

    @staticmethod
    def generate_key_hex() -> str:
        """Generate a cryptographically secure 256-bit (32-byte) key in hex format."""
        return AESGCM.generate_key(bit_length=AES_GCM_KEY_SIZE_BITS).hex()

    @staticmethod
    def validate_key(key_hex: str) -> bytes:
        """Validate that key_hex represents a 32-byte (256-bit) cryptographic key."""
        if not key_hex or not isinstance(key_hex, str):
            raise InvalidKeyError("AES-GCM key must be provided as a non-empty hexadecimal string.")
        cleaned = key_hex.strip().replace(" ", "")
        try:
            key_bytes = bytes.fromhex(cleaned)
        except ValueError:
            raise InvalidKeyError("Key contains non-hexadecimal characters.")

        expected_bytes = AES_GCM_KEY_SIZE_BITS // 8
        if len(key_bytes) != expected_bytes:
            raise InvalidKeyError(
                f"AES-GCM-256 requires a 32-byte (64 hex characters) key. Received {len(key_bytes)} bytes."
            )
        return key_bytes

    @classmethod
    def encrypt(
        cls, plaintext: str, key_hex: str, associated_data: str = ""
    ) -> Tuple[str, Dict[str, str]]:
        """
        Encrypt plaintext with AES-GCM-256.
        Returns a versioned JSON container string and a dict of container fields.
        """
        key_bytes = cls.validate_key(key_hex)
        nonce = os.urandom(AES_GCM_NONCE_SIZE_BYTES)
        pt_bytes = plaintext.encode("utf-8")
        aad_bytes = associated_data.encode("utf-8") if associated_data else None

        aesgcm = AESGCM(key_bytes)
        # In cryptography.hazmat, AESGCM.encrypt appends the 16-byte tag to the ciphertext
        encrypted = aesgcm.encrypt(nonce, pt_bytes, aad_bytes)
        ciphertext = encrypted[:-AES_GCM_TAG_SIZE_BYTES]
        tag = encrypted[-AES_GCM_TAG_SIZE_BYTES:]

        container = {
            "version": CONTAINER_FORMAT_VERSION,
            "algorithm": "AES-GCM-256",
            "nonce_b64": base64.b64encode(nonce).decode("ascii"),
            "tag_b64": base64.b64encode(tag).decode("ascii"),
            "ciphertext_b64": base64.b64encode(ciphertext).decode("ascii"),
            "aad_b64": base64.b64encode(aad_bytes).decode("ascii") if aad_bytes else "",
        }
        container_json = json.dumps(container, indent=2)
        return container_json, container

    @classmethod
    def decrypt(cls, container_json: str, key_hex: str) -> str:
        """
        Decrypt a versioned AES-GCM container JSON.
        Throws AuthenticationError if the tag does not match or data was modified.
        """
        key_bytes = cls.validate_key(key_hex)
        if not container_json or not isinstance(container_json, str):
            raise ValidationError("Container input must be a non-empty string.")

        try:
            container = json.loads(container_json.strip())
        except json.JSONDecodeError:
            raise ValidationError("Invalid JSON format. Expected an AES-GCM container envelope.")

        # Validate mandatory container keys
        for required_field in ("version", "algorithm", "nonce_b64", "tag_b64", "ciphertext_b64"):
            if required_field not in container:
                raise ValidationError(f"Missing required container field: '{required_field}'.")

        if container.get("algorithm") != "AES-GCM-256":
            raise ValidationError(
                f"Unsupported container algorithm '{container.get('algorithm')}'. Expected 'AES-GCM-256'."
            )

        try:
            nonce = base64.b64decode(container["nonce_b64"])
            tag = base64.b64decode(container["tag_b64"])
            ciphertext = base64.b64decode(container["ciphertext_b64"])
            aad = (
                base64.b64decode(container.get("aad_b64", "")) if container.get("aad_b64") else None
            )
        except Exception as e:
            raise ValidationError(f"Failed to decode base64 fields from container: {e}")

        if len(nonce) != AES_GCM_NONCE_SIZE_BYTES:
            raise ValidationError(
                f"Invalid nonce length: expected {AES_GCM_NONCE_SIZE_BYTES} bytes, got {len(nonce)}."
            )
        if len(tag) != AES_GCM_TAG_SIZE_BYTES:
            raise ValidationError(
                f"Invalid tag length: expected {AES_GCM_TAG_SIZE_BYTES} bytes, got {len(tag)}."
            )

        aesgcm = AESGCM(key_bytes)
        # Reconstruct full payload (ciphertext + tag) for AESGCM decrypt method
        full_payload = ciphertext + tag

        try:
            pt_bytes = aesgcm.decrypt(nonce, full_payload, aad)
            return pt_bytes.decode("utf-8")
        except InvalidTag:
            raise AuthenticationError(
                "AES-GCM authentication verification failed! The ciphertext or tag has been modified, "
                "or the provided secret key is incorrect."
            )
        except UnicodeDecodeError:
            raise ValidationError("Decrypted data is not valid UTF-8 plaintext.")
