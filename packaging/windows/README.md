# Windows Packaging Details

- Target Architecture: Windows x64 (Windows 10 / 11)
- Distribution format: Standalone folder (`--onedir`) containing `HAXMED-CryptoLab.exe` and Qt DLLs
- Invocation: `powershell -File scripts/build_windows.ps1`
- Dependencies bundled: PySide6 (QtCore, QtGui, QtWidgets), cryptography (OpenSSL DLLs), bcrypt, argon2-cffi.
