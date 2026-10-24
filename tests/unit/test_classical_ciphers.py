"""Unit tests for classical cryptographic ciphers."""

import pytest

from haxmed_cryptolab.core.exceptions import ValidationError
from haxmed_cryptolab.engines.classical.atbash import AtbashCipher
from haxmed_cryptolab.engines.classical.caesar import CaesarCipher
from haxmed_cryptolab.engines.classical.substitution import SubstitutionCipher
from haxmed_cryptolab.engines.classical.transposition import TranspositionCipher
from haxmed_cryptolab.engines.classical.vigenere import VigenereCipher


class TestCaesarCipher:
    def test_caesar_encrypt_decrypt(self):
        pt = "Hello, World! 123"
        shift = 3
        ct = CaesarCipher.encrypt(pt, shift)
        assert ct == "Khoor, Zruog! 123"
        dec = CaesarCipher.decrypt(ct, shift)
        assert dec == pt

    def test_caesar_large_and_negative_shift(self):
        pt = "Cryptography"
        assert CaesarCipher.encrypt(pt, 29) == CaesarCipher.encrypt(pt, 3)
        assert CaesarCipher.encrypt(pt, -3) == CaesarCipher.decrypt(pt, 3)

    def test_caesar_invalid_shift(self):
        with pytest.raises(ValidationError):
            CaesarCipher.validate_shift("invalid_shift")

    def test_caesar_brute_force(self):
        ct = "Khoor"
        candidates = CaesarCipher.brute_force(ct)
        assert len(candidates) == 25
        # At shift 3, decryption of 'Khoor' should be 'Hello'
        shift3_text = [text for s, text in candidates if s == 3][0]
        assert shift3_text == "Hello"


class TestAtbashCipher:
    def test_atbash_involution(self):
        pt = "Attack at Dawn! 123"
        ct = AtbashCipher.encrypt(pt)
        assert ct == "Zggzxp zg Wzdm! 123"
        assert AtbashCipher.decrypt(ct) == pt


class TestVigenereCipher:
    def test_vigenere_round_trip(self):
        pt = "ATTACKATDAWN"
        key = "LEMON"
        ct = VigenereCipher.encrypt(pt, key)
        assert ct == "LXFOPVEFRNHR"
        dec = VigenereCipher.decrypt(ct, key)
        assert dec == pt

    def test_vigenere_preserves_spaces_and_case(self):
        pt = "Hello, World!"
        key = "KEY"
        ct = VigenereCipher.encrypt(pt, key)
        assert VigenereCipher.decrypt(ct, key) == pt

    def test_vigenere_invalid_key(self):
        with pytest.raises(ValidationError):
            VigenereCipher.validate_key("12345!@#")
        with pytest.raises(ValidationError):
            VigenereCipher.validate_key("")


class TestSubstitutionCipher:
    def test_substitution_round_trip(self):
        key = "QWERTYUIOPASDFGHJKLZXCVBNM"
        pt = "The Quick Brown Fox Jumps Over 123 Lazy Dogs!"
        ct = SubstitutionCipher.encrypt(pt, key)
        dec = SubstitutionCipher.decrypt(ct, key)
        assert dec == pt

    def test_substitution_invalid_keys(self):
        # Too short
        with pytest.raises(ValidationError):
            SubstitutionCipher.validate_key("ABC")
        # Duplicate letters
        with pytest.raises(ValidationError):
            SubstitutionCipher.validate_key("AAAAAAAAAAAAAAAAAAAAAAAAAA")
        # Non-alphabetic
        with pytest.raises(ValidationError):
            SubstitutionCipher.validate_key("QWERTYUIOPASDFGHJKLZXCVBN1")


class TestTranspositionCipher:
    def test_transposition_round_trip(self):
        pt = "COMMON_SENSE_TOLD_US_TO_FLEE_NOW"
        key = 5
        ct = TranspositionCipher.encrypt(pt, key)
        dec = TranspositionCipher.decrypt(ct, key)
        assert dec == pt

    def test_transposition_short_text(self):
        pt = "HAX"
        key = 10
        ct = TranspositionCipher.encrypt(pt, key)
        assert TranspositionCipher.decrypt(ct, key) == pt

    def test_transposition_invalid_key(self):
        with pytest.raises(ValidationError):
            TranspositionCipher.validate_key(1)
        with pytest.raises(ValidationError):
            TranspositionCipher.validate_key("zero")
