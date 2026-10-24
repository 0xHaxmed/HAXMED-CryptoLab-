# Changelog

All notable changes to **HAXMED CryptoLab** will be documented in this file.

## [1.0.0] - 2026-10-24

### Added
- **Core Architecture**: Modular Qt (PySide6) desktop architecture with clear separation between UI, Services, Engines, Models, and Storage.
- **Bilingual Interface**: Full English (LTR) and Arabic (RTL) support with dynamic runtime language switching.
- **Branded Design System**: Professional dark charcoal theme with deep crimson accents, restrained borders, and accessible typography.
- **Module A - Dashboard**: System info, quick actions, educational crypto highlights, active worker status.
- **Module B - Encryption Studio**:
  - Classical: Caesar (with brute-force shift explorer), Atbash, Vigenère, Monoalphabetic Substitution, Columnar Transposition.
  - Modern: AES-GCM-256 (authenticated encryption, versioned container format, tamper detection), RSA-OAEP-2048/4096 (key generation, public encryption, private decryption), RSA-PSS (digital signing and verification).
- **Module C - Hash Workbench**:
  - SHA-256, SHA-512, SHA3-256, SHA3-512, MD5, SHA-1.
  - Text and chunked file hashing with memory safety.
  - Constant-time hash comparison (Match / No Match / Invalid format).
  - Cautious hash identification (format analysis, length, prefix matching).
  - Comprehensive educational notes on collisions and preimage resistance.
- **Module D - Authorized Hash Recovery Lab**:
  - Wordlist loader with encoding checks and candidate count.
  - Configurable mutation rules (case, prefix, suffix, numeric padding).
  - Multi-format adapters: hex digests, bcrypt, Argon2id.
  - Non-blocking background worker with progress, elapsed time, cancellation.
  - Sanitized summary reporting and strict authorization banner.
- **Module E - Classical Cipher Analyzer**:
  - Frequency distribution analysis (English reference comparison).
  - Caesar shift enumeration matrix with statistical scoring.
- **Module F - History & Reports**:
  - Privacy-preserving SQLite audit log (disabled by default, no plaintexts/keys stored).
  - Export reports to TXT and JSON.
- **Module G - Settings**:
  - Dark/Light theme switching, Language selection (English / Arabic), Privacy controls, Reset defaults.
- **Automated Test Suite**: Extensive unit, integration, UI, and security tests.
- **Cross-Platform Packaging**: Windows PowerShell and Linux bash PyInstaller packaging scripts.
