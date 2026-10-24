"""Unit tests for modern symmetric and asymmetric cryptographic engines."""

import json

import pytest

from haxmed_cryptolab.core.exceptions import AuthenticationError, InvalidKeyError, ValidationError
from haxmed_cryptolab.engines.asymmetric.rsa_oaep import RSAOAEPEngine
from haxmed_cryptolab.engines.asymmetric.rsa_pss import RSAPSSEngine
from haxmed_cryptolab.engines.symmetric.aes_gcm import AESGCMEngine


class TestAESGCM:
    def test_key_generation(self):
        key = AESGCMEngine.generate_key_hex()
        assert len(key) == 64
        bytes_key = bytes.fromhex(key)
        assert len(bytes_key) == 32

    def test_encrypt_decrypt_round_trip(self):
        key = AESGCMEngine.generate_key_hex()
        pt = "Top Secret Information: 12345"
        aad = "Header-Metadata-V1"
        container_json, meta = AESGCMEngine.encrypt(pt, key, aad)

        assert meta["algorithm"] == "AES-GCM-256"
        decrypted = AESGCMEngine.decrypt(container_json, key)
        assert decrypted == pt

    def test_tampered_ciphertext_detection(self):
        key = AESGCMEngine.generate_key_hex()
        pt = "Authentic Message"
        container_json, _ = AESGCMEngine.encrypt(pt, key)

        data = json.loads(container_json)
        # Flip a character in base64 ciphertext
        raw_ct = list(data["ciphertext_b64"])
        raw_ct[0] = "B" if raw_ct[0] != "B" else "A"
        data["ciphertext_b64"] = "".join(raw_ct)
        tampered_json = json.dumps(data)

        with pytest.raises(AuthenticationError):
            AESGCMEngine.decrypt(tampered_json, key)

    def test_wrong_key_rejection(self):
        key1 = AESGCMEngine.generate_key_hex()
        key2 = AESGCMEngine.generate_key_hex()
        container_json, _ = AESGCMEngine.encrypt("Message", key1)

        with pytest.raises(AuthenticationError):
            AESGCMEngine.decrypt(container_json, key2)

    def test_invalid_key_length(self):
        with pytest.raises(InvalidKeyError):
            AESGCMEngine.validate_key("abcd1234")


class TestRSAOAEP:
    def test_keypair_generation(self):
        priv_pem, pub_pem = RSAOAEPEngine.generate_key_pair(2048)
        assert "-----BEGIN PRIVATE KEY-----" in priv_pem
        assert "-----BEGIN PUBLIC KEY-----" in pub_pem

    def test_encrypt_decrypt_round_trip(self):
        priv_pem, pub_pem = RSAOAEPEngine.generate_key_pair(2048)
        pt = "Hello RSA-OAEP with SHA-256!"
        ct_b64 = RSAOAEPEngine.encrypt(pt, pub_pem)
        decrypted = RSAOAEPEngine.decrypt(ct_b64, priv_pem)
        assert decrypted == pt

    def test_plaintext_size_limit_rejection(self):
        _, pub_pem = RSAOAEPEngine.generate_key_pair(2048)
        # Max OAEP SHA-256 for 2048 is 190 bytes
        oversized = "A" * 250
        with pytest.raises(ValidationError) as exc:
            RSAOAEPEngine.encrypt(oversized, pub_pem)
        assert "Plaintext too long" in str(exc.value)


class TestRSAPSS:
    def test_sign_and_verify_valid(self):
        priv_pem, pub_pem = RSAOAEPEngine.generate_key_pair(2048)
        msg = "Transaction: Transfer $100 to Alice"
        sig_b64 = RSAPSSEngine.sign(msg, priv_pem)
        assert len(sig_b64) > 0

        is_valid, desc = RSAPSSEngine.verify(msg, sig_b64, pub_pem)
        assert is_valid is True
        assert "VALID" in desc

    def test_altered_message_verification_fails(self):
        priv_pem, pub_pem = RSAOAEPEngine.generate_key_pair(2048)
        msg = "Original Message"
        sig_b64 = RSAPSSEngine.sign(msg, priv_pem)

        altered_msg = "Altered Message!"
        is_valid, desc = RSAPSSEngine.verify(altered_msg, sig_b64, pub_pem)
        assert is_valid is False
        assert "INVALID" in desc
