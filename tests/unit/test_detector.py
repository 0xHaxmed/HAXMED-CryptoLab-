"""Unit tests for the Smart Cryptographic Auto-Detector."""

from haxmed_cryptolab.engines.analysis.detector import SmartDetector
from haxmed_cryptolab.engines.classical.caesar import CaesarCipher
from haxmed_cryptolab.engines.symmetric.aes_gcm import AESGCMEngine
from haxmed_cryptolab.models import DetectedCategory


class TestSmartDetector:
    def test_detect_aes_gcm_container(self):
        key = AESGCMEngine.generate_key_hex()
        container_json, _ = AESGCMEngine.encrypt("Secret Database Password", key)

        report = SmartDetector.analyze(container_json)
        assert report.category == DetectedCategory.AES_GCM_CONTAINER
        assert report.suggested_algorithm == "AES-GCM-256"
        assert report.confidence == "HIGH"
        assert report.suggested_action == "DECRYPT_AES"

    def test_detect_rsa_keys(self):
        pub_pem = (
            "-----BEGIN PUBLIC KEY-----\n"
            "MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAz5...\n"
            "-----END PUBLIC KEY-----"
        )
        report_pub = SmartDetector.analyze(pub_pem)
        assert report_pub.category == DetectedCategory.PEM_KEY
        assert "Public Key" in report_pub.suggested_algorithm

        priv_pem = (
            "-----BEGIN PRIVATE KEY-----\n"
            "MIIEvgIBADANBgkqhkiG9w0BAQEFAASCBKgwggSkAgEAAoIBAQD...\n"
            "-----END PRIVATE KEY-----"
        )
        report_priv = SmartDetector.analyze(priv_pem)
        assert report_priv.category == DetectedCategory.PEM_KEY
        assert "Private Key" in report_priv.suggested_algorithm

    def test_detect_bcrypt_hash(self):
        b_hash = "$2b$12$e8POdGlHFqcuhG7UmUqEuOG/9k/D8sC0z.6K29qN0Pj.j7B4iT/y2"
        report = SmartDetector.analyze(b_hash)
        assert report.category == DetectedCategory.HASH
        assert report.suggested_algorithm == "Bcrypt"
        assert report.suggested_action == "RECOVERY_LAB"

    def test_detect_argon2_hash(self):
        a_hash = "$argon2id$v=19$m=65536,t=3,p=4$c29tZXNhbHQ$RdescudvJCsgqlfreSAeYQ"
        report = SmartDetector.analyze(a_hash)
        assert report.category == DetectedCategory.HASH
        assert "Argon2" in report.suggested_algorithm
        assert report.suggested_action == "RECOVERY_LAB"

    def test_detect_hex_digests(self):
        # 32 chars = MD5
        md5_digest = "d41d8cd98f00b204e9800998ecf8427e"
        rep_md5 = SmartDetector.analyze(md5_digest)
        assert rep_md5.category == DetectedCategory.HASH
        assert "MD5" in rep_md5.suggested_algorithm

        # 64 chars = SHA-256
        sha256_digest = "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"
        rep_sha = SmartDetector.analyze(sha256_digest)
        assert rep_sha.category == DetectedCategory.HASH
        assert "SHA-256" in rep_sha.suggested_algorithm

    def test_detect_caesar_cipher(self):
        english_pt = "The quick brown fox jumps over the lazy dog and the animals in the forest are watching carefully."
        shift = 4
        caesar_ct = CaesarCipher.encrypt(english_pt, shift)

        report = SmartDetector.analyze(caesar_ct)
        assert report.category == DetectedCategory.CAESAR_CIPHER
        assert f"Shift {shift}" in report.suggested_algorithm
        assert report.suggested_action == "DECRYPT_CAESAR"
        assert report.metadata.get("shift") == shift
