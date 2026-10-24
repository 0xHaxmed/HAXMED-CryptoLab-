"""Unit tests for recovery rules, adapters, frequency analysis, and Caesar ranking."""

import hashlib

import bcrypt
import pytest
from argon2 import PasswordHasher

from haxmed_cryptolab.core.exceptions import ValidationError
from haxmed_cryptolab.engines.analysis.caesar_analyzer import CaesarAnalyzer
from haxmed_cryptolab.engines.analysis.frequency import FrequencyAnalyzer
from haxmed_cryptolab.engines.classical.caesar import CaesarCipher
from haxmed_cryptolab.engines.recovery.adapters import (
    Argon2idAdapter,
    BcryptAdapter,
    RawDigestAdapter,
)
from haxmed_cryptolab.engines.recovery.rules import CandidateMutator, RuleConfig


class TestRecoveryRulesAndAdapters:
    def test_candidate_mutations(self):
        cfg = RuleConfig(
            apply_original=True,
            apply_lowercase=True,
            apply_uppercase=True,
            apply_capitalize=True,
            prefix="adm_",
            suffix="!",
            append_numeric_range_end=2,
        )
        mutations = list(CandidateMutator.generate_mutations("Secret", cfg))
        # Expected to include 'adm_Secret!', 'adm_Secret!0', 'adm_Secret!1', 'adm_Secret!2', 'adm_secret!', etc.
        assert "adm_Secret!" in mutations
        assert "adm_Secret!1" in mutations
        assert "adm_secret!" in mutations
        assert "adm_SECRET!" in mutations

    def test_rule_config_bounds(self):
        invalid_cfg = RuleConfig(append_numeric_range_end=50000)
        with pytest.raises(ValidationError):
            list(CandidateMutator.generate_mutations("test", invalid_cfg))

    def test_raw_digest_adapter(self):
        adapter = RawDigestAdapter("SHA-256")
        target = hashlib.sha256(b"haxmed").hexdigest()
        assert adapter.verify("haxmed", target) is True
        assert adapter.verify("wrong", target) is False

    def test_bcrypt_adapter(self):
        adapter = BcryptAdapter()
        # Generate genuine synthetic Bcrypt hash with low rounds for test speed
        salt = bcrypt.gensalt(rounds=4)
        target = bcrypt.hashpw(b"testpass123", salt).decode("ascii")

        assert adapter.verify("testpass123", target) is True
        assert adapter.verify("wrongpass", target) is False

    def test_argon2_adapter(self):
        adapter = Argon2idAdapter()
        ph = PasswordHasher(time_cost=1, memory_cost=1024, parallelism=1)
        target = ph.hash("argon_secret")

        assert adapter.verify("argon_secret", target) is True
        assert adapter.verify("wrong_secret", target) is False


class TestCryptanalysis:
    def test_frequency_calculation(self):
        text = "AAAAABBBCC"
        counts, pcts, total = FrequencyAnalyzer.calculate_frequencies(text)
        assert total == 10
        assert counts["A"] == 5
        assert pcts["A"] == 50.0
        assert counts["B"] == 3
        assert pcts["B"] == 30.0

    def test_index_of_coincidence(self):
        # Monolithic single letter has maximum coincidence = 1.0
        mono = "A" * 50
        assert pytest.approx(FrequencyAnalyzer.calculate_index_of_coincidence(mono), 0.01) == 1.0

    def test_caesar_shift_ranking(self):
        # Meaningful English sentence
        pt = "The quick brown fox jumps over the lazy dog and runs across the field."
        shift = 7
        ct = CaesarCipher.encrypt(pt, shift)

        candidates = CaesarAnalyzer.analyze_all_shifts(ct)
        # Shift 7 must decrypt to the original text and should rank #1 or very top due to Chi-Squared fit
        assert candidates[0].shift == 7
        assert candidates[0].plaintext == pt
