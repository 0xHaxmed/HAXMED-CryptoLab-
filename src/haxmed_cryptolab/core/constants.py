"""Application-wide constants, branding, and defaults."""

import os
from pathlib import Path

APP_NAME = "HAXMED CryptoLab"
APP_SLOGAN = "Professional Cryptography & Cryptanalysis Toolkit"
APP_VERSION = "1.0.0"
APP_AUTHOR = "HAXMED Security Engineering"
APP_LICENSE = "MIT"
SUPPORTED_PLATFORMS = ("Windows", "Linux")

# Directory paths: prefer workspace local or environment override to avoid unprivileged home dir writes
BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent
_env_data_dir = os.environ.get("HAXMED_DATA_DIR")
if _env_data_dir:
    USER_DATA_DIR = Path(_env_data_dir)
else:
    USER_DATA_DIR = BASE_DIR / ".data"

try:
    USER_DATA_DIR.mkdir(parents=True, exist_ok=True)
except Exception:
    pass

DB_PATH = USER_DATA_DIR / "cryptolab.db"
CONFIG_FILE_PATH = USER_DATA_DIR / "config.json"

# UI Defaults
DEFAULT_THEME = "dark"
DEFAULT_LANGUAGE = "en"  # "en" or "ar"

# Modern Cryptography Constants
AES_GCM_KEY_SIZE_BITS = 256
AES_GCM_NONCE_SIZE_BYTES = 12  # 96 bits recommended for GCM
AES_GCM_TAG_SIZE_BYTES = 16  # 128 bits
CONTAINER_FORMAT_VERSION = "1.0"

RSA_KEY_SIZES = (2048, 3072, 4096)
RSA_DEFAULT_KEY_SIZE = 2048

# Hash Workbench Supported Algorithms
SUPPORTED_HASH_ALGORITHMS = [
    "SHA-256",
    "SHA-512",
    "SHA3-256",
    "SHA3-512",
    "MD5",
    "SHA-1",
]

LEGACY_INSECURE_HASHES = {"MD5", "SHA-1"}

# Recovery Lab Supported Adapters
RECOVERY_ADAPTERS = ["Raw Digest", "Bcrypt", "Argon2id"]
