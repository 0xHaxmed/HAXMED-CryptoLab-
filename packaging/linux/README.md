# Linux Packaging Details

- Target Architecture: Linux x86_64 (glibc 2.31+)
- Distribution format: Standalone folder (`--onedir`) containing executable binary and shared objects
- Invocation: `bash scripts/build_linux.sh`
- Dependencies bundled: PySide6 (QtCore, QtGui, QtWidgets), cryptography (libcrypto, libssl), bcrypt, argon2-cffi.
