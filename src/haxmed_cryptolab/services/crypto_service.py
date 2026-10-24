"""Service coordinating classical and modern cryptographic operations."""

import time
from typing import Optional, Tuple

from haxmed_cryptolab.core.config import ConfigManager
from haxmed_cryptolab.engines.asymmetric.rsa_oaep import RSAOAEPEngine
from haxmed_cryptolab.engines.asymmetric.rsa_pss import RSAPSSEngine
from haxmed_cryptolab.engines.classical.atbash import AtbashCipher
from haxmed_cryptolab.engines.classical.caesar import CaesarCipher
from haxmed_cryptolab.engines.classical.substitution import SubstitutionCipher
from haxmed_cryptolab.engines.classical.transposition import TranspositionCipher
from haxmed_cryptolab.engines.classical.vigenere import VigenereCipher
from haxmed_cryptolab.engines.symmetric.aes_gcm import AESGCMEngine
from haxmed_cryptolab.models import CryptoResult
from haxmed_cryptolab.security.validator import validate_text_input
from haxmed_cryptolab.storage.history_repository import HistoryRepository


class CryptoService:
    """Orchestrates encryption, decryption, signing, and key generation."""

    def __init__(
        self,
        history_repo: Optional[HistoryRepository] = None,
        config_mgr: Optional[ConfigManager] = None,
    ):
        self.history_repo = history_repo or HistoryRepository()
        self.config_mgr = config_mgr or ConfigManager()

    def _log_audit(
        self, operation: str, algorithm: str, status: str, duration_ms: float, details: str = ""
    ):
        """Log sanitized history record if history is enabled in configuration."""
        if self.config_mgr.config.enable_history:
            self.history_repo.add_record(
                operation_type=operation,
                algorithm=algorithm,
                status=status,
                duration_ms=duration_ms,
                details=details,
            )

    # --- Classical Ciphers ---

    def process_caesar(self, text: str, shift: int, decrypt: bool = False) -> CryptoResult:
        t0 = time.perf_counter()
        op = "DECRYPT" if decrypt else "ENCRYPT"
        try:
            valid_text = validate_text_input(text)
            out = (
                CaesarCipher.decrypt(valid_text, shift)
                if decrypt
                else CaesarCipher.encrypt(valid_text, shift)
            )
            dt_ms = (time.perf_counter() - t0) * 1000
            self._log_audit(op, "Caesar", "SUCCESS", dt_ms, f"Shift={shift}")
            return CryptoResult(
                success=True, data=out, algorithm="Caesar", operation=op, execution_time_ms=dt_ms
            )
        except Exception as e:
            dt_ms = (time.perf_counter() - t0) * 1000
            self._log_audit(op, "Caesar", "FAILED", dt_ms, str(e))
            return CryptoResult(
                success=False,
                data="",
                algorithm="Caesar",
                operation=op,
                error_message=str(e),
                execution_time_ms=dt_ms,
            )

    def process_atbash(self, text: str) -> CryptoResult:
        t0 = time.perf_counter()
        try:
            valid_text = validate_text_input(text)
            out = AtbashCipher.transform(valid_text)
            dt_ms = (time.perf_counter() - t0) * 1000
            self._log_audit("TRANSFORM", "Atbash", "SUCCESS", dt_ms)
            return CryptoResult(
                success=True,
                data=out,
                algorithm="Atbash",
                operation="TRANSFORM",
                execution_time_ms=dt_ms,
            )
        except Exception as e:
            dt_ms = (time.perf_counter() - t0) * 1000
            self._log_audit("TRANSFORM", "Atbash", "FAILED", dt_ms, str(e))
            return CryptoResult(
                success=False,
                data="",
                algorithm="Atbash",
                operation="TRANSFORM",
                error_message=str(e),
                execution_time_ms=dt_ms,
            )

    def process_vigenere(self, text: str, key: str, decrypt: bool = False) -> CryptoResult:
        t0 = time.perf_counter()
        op = "DECRYPT" if decrypt else "ENCRYPT"
        try:
            valid_text = validate_text_input(text)
            out = (
                VigenereCipher.decrypt(valid_text, key)
                if decrypt
                else VigenereCipher.encrypt(valid_text, key)
            )
            dt_ms = (time.perf_counter() - t0) * 1000
            self._log_audit(op, "Vigenere", "SUCCESS", dt_ms)
            return CryptoResult(
                success=True, data=out, algorithm="Vigenere", operation=op, execution_time_ms=dt_ms
            )
        except Exception as e:
            dt_ms = (time.perf_counter() - t0) * 1000
            self._log_audit(op, "Vigenere", "FAILED", dt_ms, str(e))
            return CryptoResult(
                success=False,
                data="",
                algorithm="Vigenere",
                operation=op,
                error_message=str(e),
                execution_time_ms=dt_ms,
            )

    def process_substitution(self, text: str, key: str, decrypt: bool = False) -> CryptoResult:
        t0 = time.perf_counter()
        op = "DECRYPT" if decrypt else "ENCRYPT"
        try:
            valid_text = validate_text_input(text)
            out = (
                SubstitutionCipher.decrypt(valid_text, key)
                if decrypt
                else SubstitutionCipher.encrypt(valid_text, key)
            )
            dt_ms = (time.perf_counter() - t0) * 1000
            self._log_audit(op, "Monoalphabetic Substitution", "SUCCESS", dt_ms)
            return CryptoResult(
                success=True,
                data=out,
                algorithm="Monoalphabetic Substitution",
                operation=op,
                execution_time_ms=dt_ms,
            )
        except Exception as e:
            dt_ms = (time.perf_counter() - t0) * 1000
            self._log_audit(op, "Monoalphabetic Substitution", "FAILED", dt_ms, str(e))
            return CryptoResult(
                success=False,
                data="",
                algorithm="Monoalphabetic Substitution",
                operation=op,
                error_message=str(e),
                execution_time_ms=dt_ms,
            )

    def process_transposition(self, text: str, key: str, decrypt: bool = False) -> CryptoResult:
        t0 = time.perf_counter()
        op = "DECRYPT" if decrypt else "ENCRYPT"
        try:
            valid_text = validate_text_input(text)
            out = (
                TranspositionCipher.decrypt(valid_text, key)
                if decrypt
                else TranspositionCipher.encrypt(valid_text, key)
            )
            dt_ms = (time.perf_counter() - t0) * 1000
            self._log_audit(op, "Columnar Transposition", "SUCCESS", dt_ms)
            return CryptoResult(
                success=True,
                data=out,
                algorithm="Columnar Transposition",
                operation=op,
                execution_time_ms=dt_ms,
            )
        except Exception as e:
            dt_ms = (time.perf_counter() - t0) * 1000
            self._log_audit(op, "Columnar Transposition", "FAILED", dt_ms, str(e))
            return CryptoResult(
                success=False,
                data="",
                algorithm="Columnar Transposition",
                operation=op,
                error_message=str(e),
                execution_time_ms=dt_ms,
            )

    # --- Modern Symmetric (AES-GCM) ---

    def generate_aes_key(self) -> str:
        return AESGCMEngine.generate_key_hex()

    def encrypt_aes_gcm(self, plaintext: str, key_hex: str, aad: str = "") -> CryptoResult:
        t0 = time.perf_counter()
        try:
            valid_text = validate_text_input(plaintext)
            container_json, meta = AESGCMEngine.encrypt(valid_text, key_hex, aad)
            dt_ms = (time.perf_counter() - t0) * 1000
            self._log_audit("ENCRYPT", "AES-GCM-256", "SUCCESS", dt_ms)
            return CryptoResult(
                success=True,
                data=container_json,
                algorithm="AES-GCM-256",
                operation="ENCRYPT",
                metadata=meta,
                execution_time_ms=dt_ms,
            )
        except Exception as e:
            dt_ms = (time.perf_counter() - t0) * 1000
            self._log_audit("ENCRYPT", "AES-GCM-256", "FAILED", dt_ms, str(e))
            return CryptoResult(
                success=False,
                data="",
                algorithm="AES-GCM-256",
                operation="ENCRYPT",
                error_message=str(e),
                execution_time_ms=dt_ms,
            )

    def decrypt_aes_gcm(self, container_json: str, key_hex: str) -> CryptoResult:
        t0 = time.perf_counter()
        try:
            plaintext = AESGCMEngine.decrypt(container_json, key_hex)
            dt_ms = (time.perf_counter() - t0) * 1000
            self._log_audit("DECRYPT", "AES-GCM-256", "SUCCESS", dt_ms)
            return CryptoResult(
                success=True,
                data=plaintext,
                algorithm="AES-GCM-256",
                operation="DECRYPT",
                execution_time_ms=dt_ms,
            )
        except Exception as e:
            dt_ms = (time.perf_counter() - t0) * 1000
            self._log_audit("DECRYPT", "AES-GCM-256", "FAILED", dt_ms, str(e))
            return CryptoResult(
                success=False,
                data="",
                algorithm="AES-GCM-256",
                operation="DECRYPT",
                error_message=str(e),
                execution_time_ms=dt_ms,
            )

    # --- Modern Asymmetric (RSA-OAEP & RSA-PSS) ---

    def generate_rsa_keypair(self, key_size: int = 2048) -> Tuple[str, str]:
        return RSAOAEPEngine.generate_key_pair(key_size)

    def encrypt_rsa_oaep(self, plaintext: str, public_key_pem: str) -> CryptoResult:
        t0 = time.perf_counter()
        try:
            valid_text = validate_text_input(plaintext)
            ct_b64 = RSAOAEPEngine.encrypt(valid_text, public_key_pem)
            dt_ms = (time.perf_counter() - t0) * 1000
            self._log_audit("ENCRYPT", "RSA-OAEP", "SUCCESS", dt_ms)
            return CryptoResult(
                success=True,
                data=ct_b64,
                algorithm="RSA-OAEP",
                operation="ENCRYPT",
                execution_time_ms=dt_ms,
            )
        except Exception as e:
            dt_ms = (time.perf_counter() - t0) * 1000
            self._log_audit("ENCRYPT", "RSA-OAEP", "FAILED", dt_ms, str(e))
            return CryptoResult(
                success=False,
                data="",
                algorithm="RSA-OAEP",
                operation="ENCRYPT",
                error_message=str(e),
                execution_time_ms=dt_ms,
            )

    def decrypt_rsa_oaep(self, ciphertext_b64: str, private_key_pem: str) -> CryptoResult:
        t0 = time.perf_counter()
        try:
            pt = RSAOAEPEngine.decrypt(ciphertext_b64, private_key_pem)
            dt_ms = (time.perf_counter() - t0) * 1000
            self._log_audit("DECRYPT", "RSA-OAEP", "SUCCESS", dt_ms)
            return CryptoResult(
                success=True,
                data=pt,
                algorithm="RSA-OAEP",
                operation="DECRYPT",
                execution_time_ms=dt_ms,
            )
        except Exception as e:
            dt_ms = (time.perf_counter() - t0) * 1000
            self._log_audit("DECRYPT", "RSA-OAEP", "FAILED", dt_ms, str(e))
            return CryptoResult(
                success=False,
                data="",
                algorithm="RSA-OAEP",
                operation="DECRYPT",
                error_message=str(e),
                execution_time_ms=dt_ms,
            )

    def sign_rsa_pss(self, message: str, private_key_pem: str) -> CryptoResult:
        t0 = time.perf_counter()
        try:
            sig_b64 = RSAPSSEngine.sign(message, private_key_pem)
            dt_ms = (time.perf_counter() - t0) * 1000
            self._log_audit("SIGN", "RSA-PSS", "SUCCESS", dt_ms)
            return CryptoResult(
                success=True,
                data=sig_b64,
                algorithm="RSA-PSS",
                operation="SIGN",
                execution_time_ms=dt_ms,
            )
        except Exception as e:
            dt_ms = (time.perf_counter() - t0) * 1000
            self._log_audit("SIGN", "RSA-PSS", "FAILED", dt_ms, str(e))
            return CryptoResult(
                success=False,
                data="",
                algorithm="RSA-PSS",
                operation="SIGN",
                error_message=str(e),
                execution_time_ms=dt_ms,
            )

    def verify_rsa_pss(self, message: str, signature_b64: str, public_key_pem: str) -> CryptoResult:
        t0 = time.perf_counter()
        try:
            is_valid, msg = RSAPSSEngine.verify(message, signature_b64, public_key_pem)
            dt_ms = (time.perf_counter() - t0) * 1000
            status = "SUCCESS" if is_valid else "INVALID_SIGNATURE"
            self._log_audit("VERIFY", "RSA-PSS", status, dt_ms, msg)
            return CryptoResult(
                success=is_valid,
                data=msg,
                algorithm="RSA-PSS",
                operation="VERIFY",
                metadata={"is_valid": is_valid},
                execution_time_ms=dt_ms,
            )
        except Exception as e:
            dt_ms = (time.perf_counter() - t0) * 1000
            self._log_audit("VERIFY", "RSA-PSS", "FAILED", dt_ms, str(e))
            return CryptoResult(
                success=False,
                data="",
                algorithm="RSA-PSS",
                operation="VERIFY",
                error_message=str(e),
                execution_time_ms=dt_ms,
            )
