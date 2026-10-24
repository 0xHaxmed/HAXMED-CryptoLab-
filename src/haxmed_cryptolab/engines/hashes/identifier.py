"""Cautious hash format analyzer and identifier."""

import re
from typing import List

from haxmed_cryptolab.models import HashIdentificationCandidate

IDENTIFICATION_DISCLAIMER = (
    "CAUTION: A hash digest is simply a fixed-length string of bytes. "
    "Multiple distinct algorithms share identical output lengths (e.g., SHA-256 and SHA3-256 both produce 64 hex characters). "
    "Therefore, identification based solely on digest length is heuristic and cannot provide mathematical certainty."
)


class HashIdentifier:
    """Cautiously analyzes hash strings and suggests candidate algorithms."""

    @classmethod
    def identify(cls, hash_str: str) -> List[HashIdentificationCandidate]:
        """Analyze format, prefix, character set, and length."""
        if not hash_str or not isinstance(hash_str, str):
            return []

        cleaned = hash_str.strip()
        candidates: List[HashIdentificationCandidate] = []

        # Check for structured password hash prefixes
        if cleaned.startswith(("$2a$", "$2b$", "$2y$", "$2x$")):
            candidates.append(
                HashIdentificationCandidate(
                    algorithm="Bcrypt",
                    bit_length=184,
                    confidence="HIGH",
                    notes="Modular Crypt Format prefix ($2b$) indicates Blowfish-based Bcrypt with embedded salt and work factor.",
                )
            )
            return candidates

        if cleaned.startswith(("$argon2id$", "$argon2i$", "$argon2d$")):
            variant = cleaned.split("$")[1] if len(cleaned.split("$")) > 1 else "argon2"
            candidates.append(
                HashIdentificationCandidate(
                    algorithm=f"Argon2 ({variant})",
                    bit_length=0,
                    confidence="HIGH",
                    notes="PHC format string for memory-hard Argon2 password hashing.",
                )
            )
            return candidates

        if cleaned.startswith("$6$"):
            candidates.append(
                HashIdentificationCandidate(
                    algorithm="SHA-512 Crypt",
                    bit_length=512,
                    confidence="HIGH",
                    notes="Unix crypt format using salted, iterated SHA-512.",
                )
            )
            return candidates

        if cleaned.startswith("$5$"):
            candidates.append(
                HashIdentificationCandidate(
                    algorithm="SHA-256 Crypt",
                    bit_length=256,
                    confidence="HIGH",
                    notes="Unix crypt format using salted, iterated SHA-256.",
                )
            )
            return candidates

        if cleaned.startswith("$1$"):
            candidates.append(
                HashIdentificationCandidate(
                    algorithm="MD5 Crypt",
                    bit_length=128,
                    confidence="HIGH",
                    notes="Legacy Unix crypt format using salted MD5.",
                )
            )
            return candidates

        # Check raw hexadecimal digests
        hex_cleaned = cleaned.replace(" ", "").replace(":", "")
        is_hex = bool(re.match(r"^[0-9a-fA-F]+$", hex_cleaned))
        length = len(hex_cleaned)

        if not is_hex:
            return [
                HashIdentificationCandidate(
                    algorithm="Unknown / Non-Hex",
                    bit_length=0,
                    confidence="LOW",
                    notes="The supplied string contains non-hexadecimal characters and does not match known MCF prefixes.",
                )
            ]

        bit_len = length * 4

        if length == 32:  # 128 bits
            candidates.extend(
                [
                    HashIdentificationCandidate(
                        algorithm="MD5",
                        bit_length=128,
                        confidence="POSSIBLE",
                        notes="Extremely common legacy 128-bit digest. Broken for collision resistance.",
                    ),
                    HashIdentificationCandidate(
                        algorithm="NTLM",
                        bit_length=128,
                        confidence="POSSIBLE",
                        notes="Windows NT LAN Manager password hash (MD4 of UTF-16LE password).",
                    ),
                ]
            )
        elif length == 40:  # 160 bits
            candidates.extend(
                [
                    HashIdentificationCandidate(
                        algorithm="SHA-1",
                        bit_length=160,
                        confidence="POSSIBLE",
                        notes="160-bit digest. Broken for collision resistance (SHAttered attack).",
                    ),
                    HashIdentificationCandidate(
                        algorithm="RIPEMD-160",
                        bit_length=160,
                        confidence="POSSIBLE",
                        notes="160-bit European cryptographic hash, commonly used in Bitcoin addresses.",
                    ),
                ]
            )
        elif length == 64:  # 256 bits
            candidates.extend(
                [
                    HashIdentificationCandidate(
                        algorithm="SHA-256",
                        bit_length=256,
                        confidence="POSSIBLE",
                        notes="Standard SHA-2 family 256-bit digest. Widely used across modern security protocols.",
                    ),
                    HashIdentificationCandidate(
                        algorithm="SHA3-256",
                        bit_length=256,
                        confidence="POSSIBLE",
                        notes="Keccak-based NIST SHA-3 standard 256-bit digest.",
                    ),
                    HashIdentificationCandidate(
                        algorithm="BLAKE2s",
                        bit_length=256,
                        confidence="POSSIBLE",
                        notes="High-performance 256-bit cryptographic hash optimized for 8 to 32-bit platforms.",
                    ),
                ]
            )
        elif length == 128:  # 512 bits
            candidates.extend(
                [
                    HashIdentificationCandidate(
                        algorithm="SHA-512",
                        bit_length=512,
                        confidence="POSSIBLE",
                        notes="Standard SHA-2 family 512-bit digest with 64-bit word operations.",
                    ),
                    HashIdentificationCandidate(
                        algorithm="SHA3-512",
                        bit_length=512,
                        confidence="POSSIBLE",
                        notes="Keccak-based NIST SHA-3 standard 512-bit digest.",
                    ),
                    HashIdentificationCandidate(
                        algorithm="BLAKE2b",
                        bit_length=512,
                        confidence="POSSIBLE",
                        notes="High-performance 512-bit cryptographic hash optimized for 64-bit platforms.",
                    ),
                ]
            )
        else:
            candidates.append(
                HashIdentificationCandidate(
                    algorithm=f"Generic Hex Digest ({bit_len} bits)",
                    bit_length=bit_len,
                    confidence="LOW",
                    notes=f"Hexadecimal string of {length} characters ({bit_len} bits). Does not match standard digest lengths (128, 160, 256, 512).",
                )
            )

        return candidates
