# HAXMED CryptoLab — User Guide

Welcome to **HAXMED CryptoLab**, a cybersecurity learning toolkit designed for hands-on experimentation with cryptography and cryptanalysis.

---

## 1. Quick Start

### Installation
Ensure Python 3.10 or higher is installed.
```bash
python -m venv .venv
# On Windows:
.venv\Scripts\activate
# On Linux:
source .venv/bin/activate

pip install -e ".[dev]"
```

### Launching the Application
```bash
python -m haxmed_cryptolab
```

---

## 2. Walkthrough by Module

### Module A — Dashboard
The Dashboard is your command center:
- **System Diagnostics**: Displays current OS, Python version, cryptography engine availability, and active background tasks.
- **Quick Navigation**: Instant links to major workflows.
- **Educational Insights**: Contextual notes covering cryptographic principles and safety guidelines.

---

### Module B — Encryption Studio

The Encryption Studio is divided into two distinct workspaces:

#### 1. Classical Ciphers (Educational Only)
- **Supported Ciphers**: Caesar, Atbash, Vigenère, Monoalphabetic Substitution, and Columnar Transposition.
- **Caesar Brute-Force Mode**: Test any Caesar ciphertext to view all 25 possible shifts along with simple English readability ratings.
- **Key Validation**: Invalid keys (e.g. non-permutation substitution keys, non-numeric transposition keys) produce clear inline validation messages rather than corrupting text.

#### 2. Modern Cryptography (Production Primitives)
- **AES-GCM (Authenticated Encryption)**:
  - Generate a secure 256-bit key or input an existing 64-character hex key.
  - Encrypts text into a versioned JSON container containing `version`, `algorithm`, `nonce_b64`, `tag_b64`, and `ciphertext_b64`.
  - Decrypts the container and automatically validates the 128-bit authentication tag. If any byte is tampered with, decryption halts with a safety alert.
- **RSA-OAEP (Public Key Encryption)**:
  - Generate 2048-bit or 4096-bit RSA key pairs.
  - Export public and private keys in standard PEM format.
  - Encrypt with recipient's Public Key, decrypt with Private Key.
  - Automatic size limit check protects against message overflow.
- **RSA-PSS (Digital Signatures)**:
  - Sign messages using your RSA Private Key.
  - Verify signatures against the message and Public Key with explicit Valid / Invalid indicators.

---

### Module C — Hash Workbench

- **Calculate**: Select an algorithm (SHA-256, SHA-512, SHA3-256, SHA3-512, MD5, SHA-1) and enter text or drag in a file. File hashing reads chunks iteratively without loading huge files into RAM.
- **Compare**:
  - Compare two raw hexadecimal digests.
  - Calculate a digest directly from text or a file and compare against an expected checksum.
  - Uses timing-attack resistant `compare_digest` for security.
- **Identify**: Enter an unknown digest to receive candidate algorithm suggestions based on bit length, encoding, and known structural prefixes.

---

### Module D — Authorized Hash Recovery Lab

> [!CAUTION]
> This laboratory workspace is strictly intended for controlled testing against owned test samples and authorized educational labs.

1. **Load Wordlist**: Load a `.txt` dictionary file (such as a sample list of common passwords). The loader displays candidate count and verifies text encoding.
2. **Select Target & Adapter**:
   - Supported: Hex digests (SHA-256, SHA-512, MD5, SHA-1), Bcrypt hashes (`$2b$...`), and Argon2id hashes (`$argon2id$...`).
3. **Configure Mutation Rules**:
   - Lowercase, Uppercase, Capitalize.
   - Prefix and Suffix addition.
   - Bounded Numeric Suffixes (e.g., 0 to 99).
4. **Run Verification**:
   - Background worker processes candidates smoothly without freezing the UI.
   - Live candidate rate, elapsed time, and progress bar updates.
   - Instant Cancel button to halt execution.
5. **Sanitized Report Export**:
   - Export an audit report containing execution statistics, timestamp, and verification outcome.

---

### Module E — Classical Cipher Analyzer

- **Letter Frequency Analysis**: Visual distribution of letter frequencies in the ciphertext compared against standard English language baselines.
- **Caesar Shift Matrix**: Automated evaluation of all 26 rotation candidates ranked by English letter frequency scores.

---

### Module F — History & Reports

- **Privacy Invariant**: History is **disabled by default**. Sensitive inputs (plaintexts, secret keys, candidate passwords) are never stored.
- **Audit Records**: When enabled, records operation type, timestamp, algorithm, and completion status.
- **Export Options**: Export audit history to formatted TXT or JSON.
- **Purge**: Single-click button to purge all local SQLite history records.

---

### Module G — Settings

- **Language**: Switch seamlessly between English (LTR) and Arabic (RTL).
- **Themes**: Switch between Dark Charcoal and Light themes.
- **Privacy**: Enable or disable operation history.
- **Defaults**: Restore default settings at any time.
