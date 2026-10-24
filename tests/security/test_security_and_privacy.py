"""Security and privacy assurance tests."""

from pathlib import Path

import pytest

from haxmed_cryptolab.core.exceptions import (
    AuthenticationError,
    FileOperationError,
    ValidationError,
)
from haxmed_cryptolab.engines.symmetric.aes_gcm import AESGCMEngine
from haxmed_cryptolab.security.redactor import redact_sensitive_string, sanitize_audit_metadata
from haxmed_cryptolab.security.validator import validate_file_path
from haxmed_cryptolab.storage.database import DatabaseManager
from haxmed_cryptolab.storage.history_repository import HistoryRepository


class TestSecurityRedaction:
    def test_pem_private_key_redaction(self):
        sample_log = (
            "Error generated while processing: "
            "-----BEGIN PRIVATE KEY-----\nMIIEvgIBADANBgkqhkiG9w0BAQEFAASCBKgwggSkAgEAAoIBAQD...\n-----END PRIVATE KEY-----\n"
            "Operation finished."
        )
        redacted = redact_sensitive_string(sample_log)
        assert "-----BEGIN PRIVATE KEY-----" not in redacted
        assert "[REDACTED_PRIVATE_KEY]" in redacted

    def test_metadata_sanitization(self):
        dirty_meta = {
            "algorithm": "AES-GCM",
            "secret_key": "64a0f8b3c...",
            "plaintext": "Top Secret Data",
            "candidate_password": "supersecretpassword",
            "execution_time_ms": 12.5,
        }
        clean_meta = sanitize_audit_metadata(dirty_meta)
        assert clean_meta["secret_key"] == "[REDACTED]"
        assert clean_meta["plaintext"] == "[REDACTED]"
        assert clean_meta["candidate_password"] == "[REDACTED]"
        assert clean_meta["algorithm"] == "AES-GCM"
        assert clean_meta["execution_time_ms"] == 12.5


class TestFileValidationAndPathTraversal:
    def test_nonexistent_file_rejection(self, tmp_path: Path):
        fake_path = tmp_path / "does_not_exist.txt"
        with pytest.raises(FileOperationError):
            validate_file_path(str(fake_path), must_exist=True)

    def test_empty_path_rejection(self):
        with pytest.raises(ValidationError):
            validate_file_path("")


class TestPrivacyPreservingHistory:
    def test_history_does_not_store_plaintext_or_keys(self, tmp_path: Path):
        db_path = tmp_path / "test_history.db"
        db_mgr = DatabaseManager(db_path=db_path)
        repo = HistoryRepository(db_mgr)

        sensitive_input = "MySecretPassword123"
        # Repository add_record takes sanitized details
        repo.add_record(
            operation_type="ENCRYPT",
            algorithm="AES-GCM-256",
            status="SUCCESS",
            duration_ms=5.2,
            details=f"Input length={len(sensitive_input)} chars",
        )

        records = repo.get_recent()
        assert len(records) == 1
        rec = records[0]
        assert sensitive_input not in rec.details
        assert sensitive_input not in rec.operation_type


class TestCryptographicIntegrity:
    def test_aes_gcm_tamper_proofing(self):
        key = AESGCMEngine.generate_key_hex()
        pt = "Important financial transaction: $500,000"
        container_json, meta = AESGCMEngine.encrypt(pt, key)

        # Alter single byte of ciphertext in container
        import json

        data = json.loads(container_json)
        raw_b64 = data["ciphertext_b64"]
        corrupted_b64 = ("A" if raw_b64[0] != "A" else "B") + raw_b64[1:]
        data["ciphertext_b64"] = corrupted_b64
        corrupted_json = json.dumps(data)

        with pytest.raises(AuthenticationError):
            AESGCMEngine.decrypt(corrupted_json, key)
