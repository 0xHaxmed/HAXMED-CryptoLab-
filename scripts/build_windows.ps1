# =====================================================================
# HAXMED CryptoLab — Windows Packaging Script (PyInstaller)
# =====================================================================

Write-Host ">>> Starting HAXMED CryptoLab Build for Windows..." -ForegroundColor Cyan

# 1. Activate Virtual Environment
if (Test-Path ".\.venv\Scripts\Activate.ps1") {
    Write-Host "[+] Activating virtual environment..." -ForegroundColor Green
    & ".\.venv\Scripts\Activate.ps1"
} else {
    Write-Warning "No virtual environment found at .venv. Proceeding with active environment."
}

# 2. Run Test Suite
Write-Host "[+] Running automated tests prior to packaging..." -ForegroundColor Green
pytest tests/ -q
if ($LASTEXITCODE -ne 0) {
    Write-Error "[-] Tests failed! Halting packaging build."
    exit 1
}

# 3. Clean previous build artifacts
Write-Host "[+] Cleaning previous build directories..." -ForegroundColor Green
if (Test-Path ".\build") { Remove-Item -Recurse -Force ".\build" }
if (Test-Path ".\dist") { Remove-Item -Recurse -Force ".\dist" }

# 4. Invoke PyInstaller
Write-Host "[+] Compiling standalone executable with PyInstaller..." -ForegroundColor Green
pyinstaller --noconfirm --onedir --windowed `
    --name "HAXMED-CryptoLab" `
    --add-data "docs;docs" `
    --collect-all "PySide6" `
    --collect-all "cryptography" `
    --collect-all "bcrypt" `
    --collect-all "argon2" `
    "src/haxmed_cryptolab/__main__.py"

if ($LASTEXITCODE -eq 0) {
    Write-Host ">>> BUILD SUCCESSFUL!" -ForegroundColor Green
    Write-Host "Executable is available at: dist\HAXMED-CryptoLab\HAXMED-CryptoLab.exe" -ForegroundColor Cyan
} else {
    Write-Error "[-] PyInstaller build failed."
    exit 1
}
