"""Integration tests for application services and subsystems."""

from pathlib import Path

import pytest

from haxmed_cryptolab.core.config import ConfigManager
from haxmed_cryptolab.engines.recovery.rules import RuleConfig
from haxmed_cryptolab.services.crypto_service import CryptoService
from haxmed_cryptolab.services.hash_service import HashService
from haxmed_cryptolab.services.recovery_service import RecoveryService
from haxmed_cryptolab.storage.database import DatabaseManager
from haxmed_cryptolab.storage.history_repository import HistoryRepository


@pytest.fixture
def temp_environment(tmp_path: Path):
    db_file = tmp_path / "integration_cryptolab.db"
    cfg_file = tmp_path / "integration_config.json"

    db_mgr = DatabaseManager(db_path=db_file)
    history_repo = HistoryRepository(db_mgr)
    config_mgr = ConfigManager(config_path=cfg_file)
    config_mgr.config.enable_history = True
    config_mgr.save(config_mgr.config)

    return {
        "db_mgr": db_mgr,
        "history_repo": history_repo,
        "config_mgr": config_mgr,
        "tmp_path": tmp_path,
    }


class TestCryptoServiceIntegration:
    def test_end_to_end_crypto_flows(self, temp_environment):
        cs = CryptoService(temp_environment["history_repo"], temp_environment["config_mgr"])

        # Caesar
        res_c = cs.process_caesar("Hello HAXMED", 5)
        assert res_c.success is True
        dec_c = cs.process_caesar(res_c.data, 5, decrypt=True)
        assert dec_c.data == "Hello HAXMED"

        # AES-GCM
        key = cs.generate_aes_key()
        res_aes = cs.encrypt_aes_gcm("Top secret payload", key)
        assert res_aes.success is True
        dec_aes = cs.decrypt_aes_gcm(res_aes.data, key)
        assert dec_aes.data == "Top secret payload"

        # RSA-OAEP
        priv, pub = cs.generate_rsa_keypair(2048)
        res_rsa = cs.encrypt_rsa_oaep("Asymmetric Hello", pub)
        assert res_rsa.success is True
        dec_rsa = cs.decrypt_rsa_oaep(res_rsa.data, priv)
        assert dec_rsa.data == "Asymmetric Hello"

        # RSA-PSS
        res_sig = cs.sign_rsa_pss("Message to authenticate", priv)
        assert res_sig.success is True
        res_ver = cs.verify_rsa_pss("Message to authenticate", res_sig.data, pub)
        assert res_ver.success is True

        # Verify operations logged in history
        history = temp_environment["history_repo"].get_recent()
        assert len(history) >= 4


class TestHashServiceIntegration:
    def test_hash_service_flows(self, temp_environment):
        hs = HashService(temp_environment["history_repo"], temp_environment["config_mgr"])

        # Text hash
        h_res = hs.hash_text("HAXMED Test", "SHA-256")
        assert len(h_res.digest_hex) == 64

        # Compare matching
        cmp_res = hs.compare_digests(h_res.digest_hex, h_res.digest_hex, "SHA-256")
        assert cmp_res.is_match is True

        # Identify format
        id_res = hs.identify_format(h_res.digest_hex)
        assert any(c.algorithm == "SHA-256" for c in id_res)


class TestRecoveryServiceIntegration:
    def test_wordlist_inspection_and_report(self, temp_environment):
        rs = RecoveryService(temp_environment["history_repo"], temp_environment["config_mgr"])
        wl_path = Path("tests/fixtures/test_wordlist.txt").resolve()

        count, samples, enc = rs.inspect_wordlist(str(wl_path))
        assert count >= 10
        assert "password" in samples
        assert enc == "utf-8"

        report_txt = rs.generate_sanitized_report(
            target_hash="955a153205aa3e35a396263ad2ad16a3bb02ebc83626e254e0a4f5fc5120668b",
            adapter_name="Raw SHA-256",
            wordlist_name="test_wordlist.txt",
            total_evaluated=10,
            elapsed_seconds=0.05,
            match=None,
            rule_config=RuleConfig(),
            format_type="txt",
        )
        assert "HAXMED CryptoLab" in report_txt
        assert "Target Hash:" in report_txt
