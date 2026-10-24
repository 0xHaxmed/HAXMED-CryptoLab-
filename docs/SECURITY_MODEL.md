# HAXMED CryptoLab — Security Model & Threat Model

## 1. Purpose & Intended Use
HAXMED CryptoLab is designed as an educational and analytical laboratory desktop application for students, penetration testers, security engineers, and software developers.

It allows users to:
- Study classical and modern cryptographic constructions.
- Verify file and message integrity through cryptographic hashes.
- Analyze classical ciphertexts using statistical techniques.
- Test recovery of owned or authorized password hashes against targeted test candidate lists.

## 2. Core Security Invariants

### 2.1 Local-First Architecture
All computations, cryptographic operations, file hashing, and candidate comparisons are conducted **exclusively on the local machine**. The software contains zero telemetry, zero analytics tracking, and zero outbound network communication channels.

### 2.2 Privacy & Sensitive Data Protection
- **No Secret Key Logging**: Private keys and symmetric keys generated in the application are held in volatile memory only for the duration of the active session or until cleared by the user.
- **Zero Plaintext History**: The History subsystem records metadata only (operation type, algorithm, timestamp, execution duration, and success/failure status). **Plaintext inputs, private keys, candidate passwords, and recovered values are strictly redacted** before any record reaches SQLite.
- **History Opt-Out**: History logging is strictly opt-in or disabled by default depending on user privacy settings.

### 2.3 Cryptographic Hygiene
- **No Homegrown Modern Crypto**: Modern primitives (AES-GCM, RSA-OAEP, RSA-PSS) are backed exclusively by standard audited libraries (`cryptography`).
- **Cryptographically Secure Randomness**: All keys, nonces, and initialization vectors are generated using `os.urandom()` via `secrets` or `cryptography.hazmat.primitives.ciphers.aead`.
- **Authenticated Encryption**: Symmetric encryption uses AES-GCM with a 96-bit random nonce and 128-bit authentication tag. Ciphertext tampering is detected immediately and rejected with an explicit error.
- **Constant-Time Comparison**: Hash verification and authentication comparisons utilize `hmac.compare_digest` to prevent timing attack side-channels.
- **Classical Cipher Disclaimers**: Classical ciphers (Caesar, Atbash, Vigenère, Substitution, Transposition) are prominently marked with security notices identifying them as insecure historical algorithms unsuitable for modern data protection.

### 2.4 Bounded Workloads in Recovery Lab
To prevent runaway memory consumption or unintentional system freezing:
- Transformation rules enforce configurable upper bounds on numeric suffixes and word lengths.
- Wordlists are streamed line-by-line rather than loaded entirely into unconstrained memory buffers.
- The user can cancel active recovery tasks instantaneously via responsive cooperative cancellation tokens.

## 3. Threat Model

| Threat | Risk | Mitigation |
| :--- | :--- | :--- |
| Memory scraping of plaintext/keys | Low to Medium | Cryptographic material is scrubbed from UI views upon user request and garbage collected promptly. |
| Inadvertent credential leak via history DB | High | Mandatory redaction pipeline removes sensitive fields before persistence. History can be purged at any time. |
| Timing attacks on hash verification | Low | `hmac.compare_digest` ensures constant-time comparison of message digests. |
| Modified ciphertext acceptance (Padding Oracle / Bit-flipping) | High | AES-GCM authenticated encryption verifies tag validity before returning plaintext. |
| Path Traversal in File I/O | Medium | Paths selected via native OS file dialogs are strictly validated for readability and safety. |
