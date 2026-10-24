"""Application error hierarchy for HAXMED CryptoLab."""


class CryptoLabError(Exception):
    """Base exception for all HAXMED CryptoLab errors."""

    def __init__(self, message: str, code: str = "ERR_GENERAL"):
        super().__init__(message)
        self.message = message
        self.code = code


class ValidationError(CryptoLabError):
    """Raised when user input, key material, or format validation fails."""

    def __init__(self, message: str, code: str = "ERR_VALIDATION"):
        super().__init__(message, code)


class CryptographicError(CryptoLabError):
    """Base exception for cryptographic failures."""

    def __init__(self, message: str, code: str = "ERR_CRYPTO"):
        super().__init__(message, code)


class AuthenticationError(CryptographicError):
    """Raised when authentication tag verification fails (tampering/wrong key)."""

    def __init__(
        self,
        message: str = "Authentication tag verification failed. Ciphertext may have been modified or key is invalid.",
        code: str = "ERR_AUTH_FAILED",
    ):
        super().__init__(message, code)


class InvalidKeyError(ValidationError):
    """Raised when a key is of invalid size, format, or characters."""

    def __init__(self, message: str, code: str = "ERR_INVALID_KEY"):
        super().__init__(message, code)


class UnsupportedAlgorithmError(CryptoLabError):
    """Raised when an algorithm is not supported."""

    def __init__(self, algorithm: str):
        super().__init__(f"Algorithm '{algorithm}' is not supported.", code="ERR_UNSUPPORTED_ALGO")
        self.algorithm = algorithm


class FileOperationError(CryptoLabError):
    """Raised when file reading, writing, or permissions fail."""

    def __init__(self, message: str, code: str = "ERR_FILE_IO"):
        super().__init__(message, code)


class TaskCancelledError(CryptoLabError):
    """Raised when an asynchronous background task is cancelled by the user."""

    def __init__(
        self, message: str = "Operation was cancelled by user.", code: str = "ERR_CANCELLED"
    ):
        super().__init__(message, code)
