@echo off
title HAXMED CryptoLab
echo Starting HAXMED CryptoLab...

if exist "dist\HAXMED-CryptoLab\HAXMED-CryptoLab.exe" (
    start "" "dist\HAXMED-CryptoLab\HAXMED-CryptoLab.exe"
) else (
    start "" ".venv\Scripts\pythonw.exe" -m haxmed_cryptolab
)
exit
