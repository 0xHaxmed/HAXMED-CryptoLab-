# HAXMED CryptoLab — Engineering Roadmap

## Status Legend
- [x] **Implemented & Verified (v1.0.0)**
- [ ] **Planned for v1.1.0+**
- [ ] **Deferred / Under Research**

---

## Module A — Dashboard
- [x] Application branding and system environment diagnostics.
- [x] Quick action shortcuts to major security studios.
- [x] Real-time task status monitor (running, completed, failed, cancelled).
- [x] Contextual educational cryptography highlights.
- [ ] System entropy pool quality indicator (Planned v1.1.0).

## Module B — Encryption Studio
- [x] Classical Ciphers:
  - [x] Caesar Cipher with shift validator and 25-shift brute force matrix.
  - [x] Atbash Cipher with bi-directional substitution.
  - [x] Vigenère Cipher with polyalphabetic key repeating engine.
  - [x] Monoalphabetic Substitution Cipher with 26-letter bijective permutation validator.
  - [x] Columnar Transposition Cipher with numeric key validator.
- [x] Modern Cryptography:
  - [x] AES-GCM-256 authenticated encryption with 96-bit random nonce and 128-bit tag.
  - [x] Versioned JSON envelope serialization format for safe transmission and storage.
  - [x] Automatic ciphertext tampering rejection.
  - [x] RSA-OAEP asymmetric encryption (2048/4096-bit) with PEM key import/export.
  - [x] RSA-PSS digital signatures and signature verification.
- [ ] ChaCha20-Poly1305 AEAD cipher support (Planned v1.1.0).
- [ ] Elliptic Curve Digital Signature Algorithm (ECDSA / Ed25519) (Planned v1.2.0).

## Module C — Hash Workbench
- [x] Multi-algorithm hashing: SHA-256, SHA-512, SHA3-256, SHA3-512, MD5, SHA-1.
- [x] Chunked streaming file hasher with progress updates and RAM safety.
- [x] Constant-time hash comparator (`hmac.compare_digest`) resisting timing leaks.
- [x] Cautious hash identification engine analyzing lengths, encodings, and prefixes.
- [x] Educational notes on collision resistance, preimages, and password hashing.
- [ ] BLAKE3 and SHAKE-128/256 extendable-output functions (Planned v1.1.0).

## Module D — Authorized Hash Recovery Lab
- [x] Wordlist parsing with text encoding validation and candidate count.
- [x] Configurable candidate transformation rules (case conversions, prefixes, suffixes, bounded numbers).
- [x] Supported adapters: Standard hex digests (SHA-256, SHA-512, MD5, SHA-1), Bcrypt, Argon2id.
- [x] Asynchronous background worker (`QThread`) with live stats, progress, and instant cancellation.
- [x] Sanitized audit report exporter (JSON & TXT).
- [x] Prominent authorization and ethical testing disclaimer banner.
- [ ] Hybrid mask attack generation (Deferred to v1.2.0).

## Module E — Classical Cipher Analyzer
- [x] Frequency analysis with English language reference baseline comparison.
- [x] Caesar rotation ranking matrix using Chi-Squared statistical distance.
- [ ] Kasiski examination and Friedman test for polyalphabetic key length estimation (Planned v1.1.0).

## Module F — History & Reports
- [x] Local SQLite database for audit records.
- [x] Privacy by design: disabled by default, zero plaintexts/keys stored.
- [x] Clear and purge history records.
- [x] Export audit logs to JSON and formatted TXT.

## Module G — Settings & UI System
- [x] Dynamic language switching: English (LTR) and Arabic (RTL).
- [x] Dual themes: Dark Charcoal with crimson accents, and Clean Light theme.
- [x] Persistent user preferences saved locally in JSON config.
- [x] Reset to default settings.
