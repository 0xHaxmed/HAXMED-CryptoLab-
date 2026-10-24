# HAXMED CryptoLab

<p align="center">
  <strong>Professional Cross-Platform Cryptography & Cryptanalysis Desktop Application</strong>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Platform-Windows%20%7C%20Linux-blue?style=flat-square" alt="Platform" />
  <img src="https://img.shields.io/badge/Language-Python%203.10+-3776AB?style=flat-square&logo=python&logoColor=white" alt="Python 3.10+" />
  <img src="https://img.shields.io/badge/GUI-PySide6%20%2F%20Qt-41CD52?style=flat-square&logo=qt&logoColor=white" alt="PySide6" />
  <img src="https://img.shields.io/badge/Security-Local%20Only-crimson?style=flat-square" alt="Local Only" />
  <img src="https://img.shields.io/badge/License-MIT-green?style=flat-square" alt="License" />
</p>

---

## 1. Overview

**HAXMED CryptoLab** is an educational and analytical desktop toolkit built by **HAXMED Security Engineering**. It is designed for students, researchers, developers, and security practitioners to study, test, and analyze classical and modern cryptographic constructions.

All operations execute **exclusively on the local machine**. The software collects zero telemetry, conducts zero outbound network calls, and never logs secret keys, plaintexts, or candidate passwords.

---

## 2. Core Modules

| Module | Features |
| :--- | :--- |
| **A. Dashboard** | System diagnostics, quick action navigation, real-time background task monitoring, educational insights. |
| **B. Encryption Studio** | **Classical**: Caesar (with 25-shift brute force explorer), Atbash, Vigenère, Substitution, Transposition.<br/>**Modern**: AES-GCM-256 (authenticated container with tamper detection), RSA-OAEP (2048/4096-bit public-key encryption), RSA-PSS (digital signing & verification). |
| **C. Hash Workbench** | Multi-digest calculation (SHA-256, SHA-512, SHA3-256, SHA3-512, MD5, SHA-1), chunked file hashing, constant-time verification, cautious format identification. |
| **D. Hash Recovery Lab** | Authorized local testbed: wordlist parsing, rule mutations (case, prefix, suffix, numbers), multi-format adapters (Hex, Bcrypt, Argon2id), non-blocking worker with instant cancellation. |
| **E. Cipher Analyzer** | Letter-frequency histograms, English baseline comparison, Caesar rotation ranking via Chi-Squared analysis. |
| **F. History & Reports** | Privacy-first SQLite audit log (disabled by default, no plaintexts/keys stored), report export (TXT/JSON), history purge. |
| **G. Settings** | English (LTR) / Arabic (RTL) live switching, Dark Charcoal & Light themes, privacy controls, defaults reset. |

---

## 3. Installation & Setup

### Prerequisites
- Python 3.10 or higher
- Git

### Setup Virtual Environment
```bash
# Clone repository
git clone https://github.com/haxmed/cryptolab.git
cd cryptolab

# Create and activate virtual environment
python -m venv .venv

# On Windows:
.\.venv\Scripts\Activate.ps1

# On Linux:
source .venv/bin/activate

# Install dependencies in editable mode
pip install -e ".[dev]"
```

---

## 4. Running the Application

Launch HAXMED CryptoLab with:
```bash
python -m haxmed_cryptolab
```
Or via the entrypoint script:
```bash
haxmed-cryptolab
```

---

## 5. Testing & Quality Gates

Run the comprehensive test suite:
```bash
pytest
```

Run code formatting and linting:
```bash
ruff check .
ruff format --check .
```

---

## 6. Packaging

Packaging scripts are provided for Windows and Linux using PyInstaller:
- **Windows**: `scripts/build_windows.ps1`
- **Linux**: `scripts/build_linux.sh`

---

## 7. Security & Ethics

HAXMED CryptoLab is strictly intended for educational exploration, defensive security assessments, and authorized testing of controlled sample data. Never analyze hashes or data without explicit authorization.

See [SECURITY.md](SECURITY.md) and [docs/SECURITY_MODEL.md](docs/SECURITY_MODEL.md) for details.

---

## 8. License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
