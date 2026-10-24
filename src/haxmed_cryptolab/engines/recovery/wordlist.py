"""Wordlist loader and validator with encoding fallback."""

from typing import Generator, List, Tuple

from haxmed_cryptolab.core.exceptions import ValidationError
from haxmed_cryptolab.security.validator import validate_file_path


class WordlistLoader:
    """Safely reads and counts candidate words from disk."""

    @staticmethod
    def count_and_sample(file_path: str, max_sample: int = 5) -> Tuple[int, List[str], str]:
        """
        Count entries in wordlist and return sample lines and detected encoding.
        Does not load the whole file into memory.
        """
        path = validate_file_path(file_path, must_exist=True)
        detected_encoding = "utf-8"

        # Try UTF-8 first, fallback to latin-1
        try:
            with open(path, "r", encoding="utf-8") as f:
                f.readline()
        except UnicodeDecodeError:
            detected_encoding = "latin-1"

        count = 0
        samples = []
        with open(path, "r", encoding=detected_encoding, errors="replace") as f:
            for line in f:
                cleaned = line.strip()
                if cleaned:
                    count += 1
                    if len(samples) < max_sample:
                        samples.append(cleaned)

        if count == 0:
            raise ValidationError(
                f"Wordlist file '{path.name}' is empty or contains only blank lines."
            )

        return count, samples, detected_encoding

    @staticmethod
    def stream_candidates(file_path: str, encoding: str = "utf-8") -> Generator[str, None, None]:
        """Yield non-empty candidate lines from the wordlist file."""
        path = validate_file_path(file_path, must_exist=True)
        with open(path, "r", encoding=encoding, errors="replace") as f:
            for line in f:
                stripped = line.strip()
                if stripped:
                    yield stripped
