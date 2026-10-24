"""RSA-PSS Digital Signature Engine."""

import base64
from typing import Tuple

from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding

from haxmed_cryptolab.core.exceptions import CryptographicError, ValidationError
from haxmed_cryptolab.engines.asymmetric.rsa_oaep import RSAOAEPEngine

DESCRIPTION = (
    "RSA-PSS (Probabilistic Signature Scheme) is a modern, provably secure digital signature scheme. "
    "Unlike deterministic padding (PKCS#1 v1.5), PSS incorporates randomized salt, defeating signature forgery attacks."
)
WORKFLOW_NOTE = (
    "Digital signatures provide authenticity, non-repudiation, and message integrity. "
    "The sender signs the hash of the message using their private key. "
    "Anyone holding the corresponding public key can mathematically verify that the message "
    "was not altered in transit."
)


class RSAPSSEngine:
    """RSA-PSS Digital Signature implementation."""

    @classmethod
    def sign(cls, message: str, private_key_pem: str) -> str:
        """
        Sign message using RSA private key with PSS padding and SHA-256.
        Returns base64-encoded digital signature.
        """
        if message is None:
            raise ValidationError("Message to sign cannot be None.")
        priv_key = RSAOAEPEngine.load_private_key(private_key_pem)
        msg_bytes = message.encode("utf-8")

        try:
            signature = priv_key.sign(
                msg_bytes,
                padding.PSS(
                    mgf=padding.MGF1(hashes.SHA256()),
                    salt_length=padding.PSS.MAX_LENGTH,
                ),
                hashes.SHA256(),
            )
            return base64.b64encode(signature).decode("ascii")
        except Exception as e:
            raise CryptographicError(f"Digital signature creation failed: {e}")

    @classmethod
    def verify(cls, message: str, signature_b64: str, public_key_pem: str) -> Tuple[bool, str]:
        """
        Verify digital signature against message using RSA public key.
        Returns (is_valid, message_description).
        """
        if message is None:
            raise ValidationError("Message to verify cannot be None.")
        if not signature_b64 or not isinstance(signature_b64, str):
            raise ValidationError("Signature must be provided as a Base64 string.")

        pub_key = RSAOAEPEngine.load_public_key(public_key_pem)
        msg_bytes = message.encode("utf-8")

        try:
            sig_bytes = base64.b64decode(signature_b64.strip())
        except Exception as e:
            raise ValidationError(f"Invalid Base64 signature encoding: {e}")

        try:
            pub_key.verify(
                sig_bytes,
                msg_bytes,
                padding.PSS(
                    mgf=padding.MGF1(hashes.SHA256()),
                    salt_length=padding.PSS.MAX_LENGTH,
                ),
                hashes.SHA256(),
            )
            return (
                True,
                "SIGNATURE VALID: The signature was created by the holder of the private key, and the message has not been altered.",
            )
        except InvalidSignature:
            return (
                False,
                "SIGNATURE INVALID: Signature does not match the message or was created by a different key.",
            )
        except Exception as e:
            return False, f"Verification error: {e}"
