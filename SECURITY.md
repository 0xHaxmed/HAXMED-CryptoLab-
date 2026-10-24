# Security Policy

## Responsible Use Notice

**HAXMED CryptoLab** is an educational and analytical toolkit designed for cybersecurity students, developers, researchers, and security professionals.

The Hash Recovery Lab and classical cryptanalysis tools are intended solely for authorized testing, controlled lab experiments, personal education, and owned data validation. **Do not use this software against systems, passwords, or data without explicit, verifiable authorization.**

## Security Principles of HAXMED CryptoLab

1. **Local-Only Processing**: All cryptography, hashing, and recovery computations occur strictly on the local machine. No keys, hashes, plaintexts, or candidates are transmitted externally.
2. **Zero Insecure History**: Sensitive information (plaintexts, private keys, candidate passwords) is never silently logged or persisted to history.
3. **Established Cryptography**: Modern cryptographic primitives rely on standard, well-audited libraries (`cryptography`, standard library `hashlib`, `bcrypt`, `argon2-cffi`). No homegrown ciphers are used for modern cryptographic security.
4. **Distinction of Classical Ciphers**: Classical algorithms (Caesar, Atbash, Vigenère, Substitution, Transposition) are explicitly labeled as historic/educational and unsafe for securing sensitive data.

## Reporting a Vulnerability

If you discover a security flaw or vulnerability within HAXMED CryptoLab, please report it responsibly by contacting the maintainers at `security@haxmed.local`.
