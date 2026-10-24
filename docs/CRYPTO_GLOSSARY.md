# HAXMED CryptoLab — Cryptography & Security Glossary

A comprehensive educational reference for terms and concepts demonstrated across HAXMED CryptoLab.

---

### 1. Fundamental Terms

#### Encryption & Decryption
- **Encryption**: The mathematical process of converting readable information (plaintext) into an unintelligible representation (ciphertext) using a cryptographic key and algorithm.
- **Decryption**: The inverse mathematical process of converting ciphertext back into its original plaintext using the authorized cryptographic key.

#### Plaintext & Ciphertext
- **Plaintext**: Unencrypted data in its original, human-readable or machine-usable format.
- **Ciphertext**: The output of an encryption algorithm, appearing completely pseudorandom to anyone without the key.

#### Key
A parameter (typically a random sequence of bits) that controls the operation of a cryptographic cipher. The secrecy of the key determines the secrecy of the encrypted message (Kerckhoffs's principle).

---

### 2. Symmetric Cryptography

#### Symmetric Encryption
A cryptographic system where the **same secret key** is used for both encrypting and decrypting data (e.g., AES-GCM, ChaCha20-Poly1305). Both parties must securely share and protect the key.

#### Nonce (Number Used Once) / IV (Initialization Vector)
A unique value supplied alongside the key to ensure that encrypting the same plaintext multiple times yields completely distinct ciphertexts.
- **Critical Rule**: For AES-GCM, **never reuse a nonce with the same key**. Nonce reuse destroys authentication guarantees and allows catastrophic plaintext recovery.

#### Authenticated Encryption with Associated Data (AEAD)
A modern encryption construction that provides **confidentiality**, **integrity**, and **authenticity** simultaneously. Examples include **AES-GCM**.
- **Authentication Tag (MAC)**: A cryptographic checksum generated during encryption that verifies the ciphertext has not been modified or corrupted in transit. If an attacker modifies even a single bit, tag verification fails and no plaintext is released.

---

### 3. Asymmetric Cryptography

#### Asymmetric Encryption (Public-Key Cryptography)
A cryptographic system utilizing a mathematically linked **key pair**:
- **Public Key**: Can be freely shared and published; used by anyone to encrypt messages or verify signatures.
- **Private Key**: Kept strictly secret by the owner; used to decrypt messages or create digital signatures.

#### RSA (Rivest–Shamir–Adleman)
An asymmetric algorithm based on the practical difficulty of factoring the product of two large prime numbers.
- **RSA-OAEP (Optimal Asymmetric Encryption Padding)**: A secure, randomized padding scheme used for RSA encryption that protects against chosen-ciphertext attacks. Plaintext size is mathematically bounded by the key modulus length minus padding overhead.
- **RSA-PSS (Probabilistic Signature Scheme)**: A modern, provably secure padding scheme for digital signatures that incorporates a cryptographic salt.

#### Digital Signature
A mathematical scheme for demonstrating the authenticity of a digital message or document. A valid signature gives the recipient reason to believe the message was created by a known sender (authentication) and has not been altered (integrity).

---

### 4. Cryptographic Hashing

#### Cryptographic Hash Function
A deterministic mathematical function that takes an arbitrary-length block of data and returns a fixed-size string of bytes (the **digest** or hash value).
- It is a **one-way function**: computing the hash from data is fast, but inverting the hash to find the original input is computationally infeasible.

#### Key Properties of Secure Hash Functions
1. **Preimage Resistance (One-Wayness)**: Given a digest $h$, it is computationally infeasible to find any message $m$ such that $\text{hash}(m) = h$.
2. **Second Preimage Resistance (Weak Collision Resistance)**: Given an input $m_1$, it is computationally infeasible to find a distinct input $m_2 \neq m_1$ such that $\text{hash}(m_1) = \text{hash}(m_2)$.
3. **Collision Resistance (Strong Collision Resistance)**: It is computationally infeasible to find *any* two distinct inputs $m_1 \neq m_2$ such that $\text{hash}(m_1) = \text{hash}(m_2)$.

#### Legacy Hash Algorithms
- **MD5** (128-bit) and **SHA-1** (160-bit): Cryptographically broken due to practical collision attacks. They should **never** be used in security-critical systems (e.g., certificates, signatures) and are provided solely for educational comparison and legacy checksum verification.

#### Password Hashing vs. General Hashing
General-purpose hash functions (like SHA-256) are designed to be extremely fast for verifying large files. Because of their speed, an attacker can compute billions of guesses per second on modern GPUs. Password storage requires **slow, memory-hard, salted Key Derivation Functions (KDFs)** such as **Argon2id** and **Bcrypt**.
- **Salt**: A cryptographically random value generated uniquely per password to defeat rainbow table attacks.

---

### 5. Classical Cryptanalysis

#### Cryptanalysis
The study of methods for obtaining the meaning of encrypted information without access to the secret key.

#### Frequency Analysis
A technique that exploits the non-uniform distribution of letters in natural languages (e.g., 'E', 'T', 'A' are the most frequent letters in English). Monoalphabetic substitution ciphers preserve letter frequency characteristics, making them easily breakable.

#### Index of Coincidence (IoC)
A statistical measure of how likely two randomly selected letters from a text will be identical. It helps determine whether a ciphertext was produced by a monoalphabetic or polyalphabetic cipher (such as Vigenère).
