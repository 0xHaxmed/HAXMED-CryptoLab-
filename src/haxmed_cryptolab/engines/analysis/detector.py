"""Smart Cryptographic Detector and Format Recognizer."""

import base64
import json
import re

from haxmed_cryptolab.engines.analysis.caesar_analyzer import CaesarAnalyzer
from haxmed_cryptolab.engines.analysis.frequency import FrequencyAnalyzer
from haxmed_cryptolab.models import DetectedCategory, DetectionReport

HEX_REGEX = re.compile(r"^[0-9a-fA-F]+$")
BASE64_REGEX = re.compile(r"^[A-Za-z0-9+/]+={0,2}$")


class SmartDetector:
    """Intelligently analyzes and classifies unknown ciphertexts, hashes, keys, and containers."""

    @classmethod
    def analyze(cls, text: str) -> DetectionReport:
        if not text or not isinstance(text, str):
            return DetectionReport(
                category=DetectedCategory.UNKNOWN,
                suggested_algorithm="Unknown",
                confidence="LOW",
                summary="Input is empty.",
                details="Please provide text or data to analyze.",
                suggested_action="NONE",
            )

        cleaned = text.strip()

        # 1. Check for AES-GCM Versioned JSON Container
        if cleaned.startswith("{") and cleaned.endswith("}"):
            try:
                data = json.loads(cleaned)
                if (
                    isinstance(data, dict)
                    and data.get("algorithm") == "AES-GCM-256"
                    and "ciphertext_b64" in data
                    and "tag_b64" in data
                    and "nonce_b64" in data
                ):
                    return DetectionReport(
                        category=DetectedCategory.AES_GCM_CONTAINER,
                        suggested_algorithm="AES-GCM-256",
                        confidence="HIGH",
                        summary="Identified: HAXMED AES-GCM-256 Authenticated Container Envelope.",
                        details=(
                            f"Version: {data.get('version', '1.0')} | "
                            f"Nonce (96-bit): {data.get('nonce_b64', '')[:16]}... | "
                            f"Auth Tag (128-bit): Present"
                        ),
                        suggested_action="DECRYPT_AES",
                        metadata=data,
                    )
            except Exception:
                pass

        # 2. Check for Standard PEM Keys
        if "-----BEGIN PUBLIC KEY-----" in cleaned:
            return DetectionReport(
                category=DetectedCategory.PEM_KEY,
                suggested_algorithm="RSA Public Key (PEM)",
                confidence="HIGH",
                summary="Identified: RSA Public Key in SubjectPublicKeyInfo PEM format.",
                details="Can be used for RSA-OAEP public-key encryption or RSA-PSS signature verification.",
                suggested_action="ENCRYPT_RSA",
            )

        if "-----BEGIN PRIVATE KEY-----" in cleaned or "-----BEGIN RSA PRIVATE KEY-----" in cleaned:
            return DetectionReport(
                category=DetectedCategory.PEM_KEY,
                suggested_algorithm="RSA Private Key (PEM)",
                confidence="HIGH",
                summary="Identified: RSA Private Key in PKCS#8 or PKCS#1 PEM format.",
                details="Can be used for RSA-OAEP private-key decryption or RSA-PSS digital signing.",
                suggested_action="DECRYPT_RSA",
            )

        # 3. Check for Structured Password Hashes (MCF / PHC prefixes)
        if cleaned.startswith(("$2a$", "$2b$", "$2y$", "$2x$")):
            return DetectionReport(
                category=DetectedCategory.HASH,
                suggested_algorithm="Bcrypt",
                confidence="HIGH",
                summary="Identified: Blowfish-based Bcrypt password hash ($2b$).",
                details="Contains embedded cost factor, 128-bit salt, and 184-bit Blowfish key.",
                suggested_action="RECOVERY_LAB",
                metadata={"adapter": "Bcrypt"},
            )

        if cleaned.startswith(("$argon2id$", "$argon2i$", "$argon2d$")):
            variant = cleaned.split("$")[1] if len(cleaned.split("$")) > 1 else "argon2id"
            return DetectionReport(
                category=DetectedCategory.HASH,
                suggested_algorithm=f"Argon2 ({variant})",
                confidence="HIGH",
                summary="Identified: Memory-hard Argon2 password hash string.",
                details="NIST/PHC winner standard for password hashing with memory-hardness.",
                suggested_action="RECOVERY_LAB",
                metadata={"adapter": "Argon2id"},
            )

        if cleaned.startswith(("$6$", "$5$", "$1$")):
            algo = (
                "SHA-512 Crypt"
                if cleaned.startswith("$6$")
                else ("SHA-256 Crypt" if cleaned.startswith("$5$") else "MD5 Crypt")
            )
            return DetectionReport(
                category=DetectedCategory.HASH,
                suggested_algorithm=algo,
                confidence="HIGH",
                summary=f"Identified: Unix Modular Crypt Format ({algo}).",
                details="Salted and iterated password hash format.",
                suggested_action="HASH_WORKBENCH",
            )

        # 4. Check for Hexadecimal Hashes
        hex_cleaned = cleaned.replace(" ", "").replace(":", "")
        if HEX_REGEX.match(hex_cleaned) and len(hex_cleaned) % 2 == 0:
            length = len(hex_cleaned)
            if length == 32:
                return DetectionReport(
                    category=DetectedCategory.HASH,
                    suggested_algorithm="MD5 / NTLM",
                    confidence="HIGH",
                    summary="Identified: 128-bit hexadecimal digest (MD5 or NTLM password hash).",
                    details="32 hexadecimal characters. Commonly used for legacy checksums and NTLM hashes.",
                    suggested_action="HASH_WORKBENCH",
                    metadata={"length": 32, "algo": "MD5"},
                )
            elif length == 40:
                return DetectionReport(
                    category=DetectedCategory.HASH,
                    suggested_algorithm="SHA-1",
                    confidence="HIGH",
                    summary="Identified: 160-bit hexadecimal digest (SHA-1).",
                    details="40 hexadecimal characters. Broken for cryptographic collision resistance.",
                    suggested_action="HASH_WORKBENCH",
                    metadata={"length": 40, "algo": "SHA-1"},
                )
            elif length == 64:
                return DetectionReport(
                    category=DetectedCategory.HASH,
                    suggested_algorithm="SHA-256",
                    confidence="HIGH",
                    summary="Identified: 256-bit hexadecimal digest (SHA-256 / SHA3-256).",
                    details="64 hexadecimal characters. Standard cryptographic hash digest.",
                    suggested_action="HASH_WORKBENCH",
                    metadata={"length": 64, "algo": "SHA-256"},
                )
            elif length == 128:
                return DetectionReport(
                    category=DetectedCategory.HASH,
                    suggested_algorithm="SHA-512",
                    confidence="HIGH",
                    summary="Identified: 512-bit hexadecimal digest (SHA-512 / SHA3-512).",
                    details="128 hexadecimal characters. SHA-2 / SHA-3 64-bit word digest.",
                    suggested_action="HASH_WORKBENCH",
                    metadata={"length": 128, "algo": "SHA-512"},
                )
            elif length >= 16:
                return DetectionReport(
                    category=DetectedCategory.HEX_BLOB,
                    suggested_algorithm="Hexadecimal Raw Data",
                    confidence="MEDIUM",
                    summary=f"Identified: Raw Hexadecimal String ({length} chars / {length // 2} bytes).",
                    details="Could be an encryption key, nonce, or non-standard hash value.",
                    suggested_action="NONE",
                )

        # 5. Check for Base64 (RSA Ciphertext or Signatures)
        if len(cleaned) >= 64 and BASE64_REGEX.match(cleaned):
            try:
                raw_bytes = base64.b64decode(cleaned)
                byte_len = len(raw_bytes)
                if byte_len in (256, 384, 512):
                    return DetectionReport(
                        category=DetectedCategory.RSA_CIPHERTEXT,
                        suggested_algorithm=f"RSA-{byte_len * 8} Ciphertext / Signature",
                        confidence="HIGH",
                        summary=f"Identified: Likely RSA-{byte_len * 8} Encrypted Ciphertext or Digital Signature.",
                        details=f"Base64-encoded binary payload of exactly {byte_len} bytes ({byte_len * 8} bits).",
                        suggested_action="DECRYPT_RSA",
                        metadata={"key_size": byte_len * 8},
                    )
            except Exception:
                pass

        # 6. Check for Classical Ciphers via Cryptanalysis (IoC & Chi-Squared)
        alpha_count = sum(1 for c in cleaned if c.isalpha())
        if alpha_count >= 12:
            counts, pcts, total = FrequencyAnalyzer.calculate_frequencies(cleaned)
            ioc = FrequencyAnalyzer.calculate_index_of_coincidence(cleaned)
            caesar_ranks = CaesarAnalyzer.analyze_all_shifts(cleaned)
            best_shift = caesar_ranks[0]

            # If Shift 0 is already natural English
            if best_shift.shift == 0 and best_shift.chi_squared < 25.0:
                return DetectionReport(
                    category=DetectedCategory.PLAIN_TEXT,
                    suggested_algorithm="Plaintext English",
                    confidence="HIGH",
                    summary="Identified: Natural English plaintext (unencrypted).",
                    details=f"Letter frequencies closely match standard English baseline (Chi-Sq: {best_shift.chi_squared:.1f}, IoC: {ioc:.4f}).",
                    suggested_action="ENCRYPT_STUDIO",
                )

            # If another Caesar rotation scores significantly better than shift 0
            shift0_score = next((c.chi_squared for c in caesar_ranks if c.shift == 0), 999.0)
            if (
                best_shift.shift != 0
                and best_shift.chi_squared < 45.0
                and (shift0_score - best_shift.chi_squared) > 20.0
            ):
                return DetectionReport(
                    category=DetectedCategory.CAESAR_CIPHER,
                    suggested_algorithm=f"Caesar Cipher (Shift {best_shift.shift})",
                    confidence="HIGH",
                    summary=f"Identified: Caesar Cipher shifted by {best_shift.shift} positions.",
                    details=(
                        f"Decryption candidate (Shift {best_shift.shift}): '{best_shift.plaintext[:60]}...' "
                        f"(Chi-Sq: {best_shift.chi_squared:.1f}, IoC: {ioc:.4f})"
                    ),
                    suggested_action="DECRYPT_CAESAR",
                    metadata={"shift": best_shift.shift, "preview": best_shift.plaintext},
                )

            # Check Monoalphabetic vs Polyalphabetic
            if ioc >= 0.058:
                return DetectionReport(
                    category=DetectedCategory.CLASSICAL_SUBSTITUTION,
                    suggested_algorithm="Monoalphabetic Substitution Cipher",
                    confidence="MEDIUM",
                    summary="Identified: Monoalphabetic Substitution Cipher.",
                    details=f"High Index of Coincidence (IoC = {ioc:.4f} ≈ English 0.0667) indicates single-alphabet substitution.",
                    suggested_action="CIPHER_ANALYZER",
                )
            elif ioc <= 0.048 and alpha_count >= 25:
                return DetectionReport(
                    category=DetectedCategory.POLYALPHABETIC_CIPHER,
                    suggested_algorithm="Polyalphabetic Cipher (Vigenère / Transposition)",
                    confidence="MEDIUM",
                    summary="Identified: Polyalphabetic Cipher (Vigenère or Transposition).",
                    details=f"Low Index of Coincidence (IoC = {ioc:.4f} ≈ Random 0.0385) indicates flattened multi-alphabet distribution.",
                    suggested_action="CIPHER_ANALYZER",
                )

        # Fallback
        return DetectionReport(
            category=DetectedCategory.UNKNOWN,
            suggested_algorithm="Unknown / Mixed Content",
            confidence="LOW",
            summary="Could not uniquely identify cryptographic type.",
            details="The input does not match known hash signatures, container headers, or standard cipher statistical profiles.",
            suggested_action="NONE",
        )
