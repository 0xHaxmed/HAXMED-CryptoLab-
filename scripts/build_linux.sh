#!/usr/bin/env bash
# =====================================================================
# HAXMED CryptoLab — Linux Packaging Script (PyInstaller)
# =====================================================================
set -e

echo ">>> Starting HAXMED CryptoLab Build for Linux..."

# 1. Activate Virtual Environment
if [ -f ".venv/bin/activate" ]; then
    echo "[+] Activating virtual environment..."
    source .venv/bin/activate
fi

# 2. Run Test Suite
echo "[+] Running automated tests..."
pytest tests/ -q

# 3. Clean previous build artifacts
echo "[+] Cleaning previous build directories..."
rm -rf build dist

# 4. Invoke PyInstaller
echo "[+] Compiling binary with PyInstaller..."
pyinstaller --noconfirm --onedir --windowed \
    --name "HAXMED-CryptoLab" \
    --add-data "docs:docs" \
    --collect-all "PySide6" \
    --collect-all "cryptography" \
    --collect-all "bcrypt" \
    --collect-all "argon2" \
    "src/haxmed_cryptolab/__main__.py"

echo ">>> BUILD SUCCESSFUL!"
echo "Binary is available at: dist/HAXMED-CryptoLab/HAXMED-CryptoLab"
